"""TripSaathi prompt architecture — Gemini wrapper.

Implements the structured-JSON prompt described in PRD §13. Falls back to a
deterministic seed itinerary when no GEMINI_API_KEY is configured, so the
demo runs offline.
"""
from __future__ import annotations

import json
import logging
import os
import re
from dataclasses import asdict
from typing import Optional

from .google_places import PlaceResult
from .google_routes import RouteMatrix
from .seed_itineraries import seed_for

log = logging.getLogger(__name__)

_API_KEY_ENV = "GEMINI_API_KEY"
_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")


SYSTEM_INSTRUCTIONS = """You are TripSaathi, SceneTrip's planning engine.
You generate structured, persona-aware travel itineraries.

Rules:
- Respect every persona constraint as a hard rule, not a suggestion.
- Use ONLY the candidate places provided. Do not invent place names.
- Each day must include a `why` field explaining why the plan fits THIS traveler.
- Output strict JSON matching the schema. No markdown. No preamble. No trailing prose.
- Use realistic travel times from the route matrix where applicable.
- Honor food preference, walking comfort, mobility needs, and budget signals.
""".strip()


def _build_prompt(
    profile: dict,
    persona_rules: dict,
    candidate_places: list[PlaceResult],
    route_matrix: RouteMatrix,
    trip: dict,
) -> str:
    schema = {
        "itinerary": [
            {
                "day_number": "int (1-based)",
                "title": "string",
                "sub": "string (subtitle)",
                "area": "string (one of the candidate place vicinities, lowercase keyword)",
                "why": "string (persona_fit_reason — 1-2 sentences explaining fit)",
                "slots": [
                    {
                        "when": "Morning|Afternoon|Evening",
                        "stops": [
                            {
                                "name": "string (must match a candidate place name OR be a travel/rest stop)",
                                "kind": "''|food|rest|travel|shop|hidden",
                                "meta": "string (price/duration/note)",
                                "place_id": "string|null (echo from candidates if applicable)",
                                "duration_min": "int|null",
                                "travel_min_to_next": "int|null",
                            }
                        ],
                    }
                ],
                "walking_minutes": "int (estimate)",
                "budget_estimate": "string (e.g. '¥¥ · ~$60')",
            }
        ]
    }

    candidates_compact = [
        {
            "name": p.name,
            "place_id": p.place_id,
            "rating": p.rating,
            "price_level": p.price_level,
            "types": p.types[:3],
            "vicinity": p.vicinity,
            "wheelchair_accessible": p.wheelchair_accessible,
        }
        for p in candidate_places
    ]
    routes_compact = [asdict(l) for l in route_matrix.legs]

    return f"""{SYSTEM_INSTRUCTIONS}

TRAVELER PROFILE:
{json.dumps(profile, ensure_ascii=False, indent=2)}

PERSONA RULES (hard constraints):
{json.dumps(persona_rules, ensure_ascii=False, indent=2)}

CANDIDATE PLACES (pick from these only):
{json.dumps(candidates_compact, ensure_ascii=False, indent=2)}

ROUTE MATRIX (sequential legs, mode={route_matrix.mode}):
{json.dumps(routes_compact, ensure_ascii=False, indent=2)}

TRIP DETAILS:
{json.dumps(trip, ensure_ascii=False, indent=2)}

OUTPUT JSON SCHEMA (return JSON exactly in this shape):
{json.dumps(schema, ensure_ascii=False, indent=2)}

Now produce {trip.get('days', 3)} days. Output ONLY JSON.
""".strip()


_JSON_BLOCK_RE = re.compile(r"\{.*\}", re.DOTALL)


def _extract_json(text: str) -> Optional[dict]:
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text, flags=re.MULTILINE).strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        m = _JSON_BLOCK_RE.search(text)
        if not m:
            return None
        try:
            return json.loads(m.group(0))
        except json.JSONDecodeError:
            return None


async def generate_itinerary(
    profile: dict,
    persona_rules: dict,
    candidate_places: list[PlaceResult],
    route_matrix: RouteMatrix,
    trip: dict,
) -> tuple[list[dict], bool]:
    """Returns (itinerary_days, used_fallback).

    `used_fallback=True` means we returned the seeded itinerary because
    Gemini was unavailable, malformed, or unconfigured.
    """
    api_key = os.getenv(_API_KEY_ENV)
    persona_id = profile.get("persona", "off_beat_explorer")
    destination = trip.get("destination", "tokyo")

    if not api_key:
        log.info("GEMINI_API_KEY not set — using seed itinerary fallback")
        return _from_seed(destination, persona_id, trip.get("days", 5)), True

    try:
        import google.generativeai as genai  # imported lazily to keep cold-start fast

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(
            _MODEL,
            generation_config={
                "response_mime_type": "application/json",
                "temperature": 0.6,
            },
        )
        prompt = _build_prompt(profile, persona_rules, candidate_places, route_matrix, trip)
        # SDK is sync — wrap in to_thread to keep the FastAPI handler non-blocking
        import asyncio

        result = await asyncio.to_thread(model.generate_content, prompt)
        parsed = _extract_json(result.text or "")
        if not parsed or "itinerary" not in parsed:
            log.warning("Gemini returned no parseable itinerary, falling back to seed")
            return _from_seed(destination, persona_id, trip.get("days", 5)), True
        days = parsed["itinerary"]
        if not isinstance(days, list) or not days:
            return _from_seed(destination, persona_id, trip.get("days", 5)), True
        return days, False
    except Exception as e:  # network/SDK/quota — never fail the request
        msg = str(e)
        if "429" in msg or "ResourceExhausted" in type(e).__name__:
            log.warning(
                "Gemini quota exhausted, falling back to seed itinerary: %s",
                msg.splitlines()[0] if msg else type(e).__name__,
            )
        else:
            log.exception("Gemini call failed, falling back to seed: %s", e)
        return _from_seed(destination, persona_id, trip.get("days", 5)), True


def _from_seed(destination: str, persona: str, days: int) -> list[dict]:
    seed = seed_for(destination, persona)
    return seed[:days] if days and days < len(seed) else seed
