"""Planner orchestration — Places → Routes → Gemini → Validator.

Also hosts the deterministic replan engine which mirrors the prototype's
applyReplan() so the demo behavior is identical with or without an LLM.
"""
from __future__ import annotations

import logging
import re

from .gemini_client import generate_itinerary
from .google_places import fetch_candidate_places
from .google_routes import estimate_route_matrix
from .persona_rules import rules_for
from .schemas import (
    DaySlot,
    ItineraryDay,
    Stop,
    TravelerProfile,
    TripDetails,
    ValidationResult,
)
from .validator import validate_itinerary

log = logging.getLogger(__name__)


# Map the long tail of free-form `kind` values an LLM might emit onto the
# strict Stop enum. Anything we can't classify becomes the empty string
# (a generic anchor) — never raise on LLM output.
_KIND_ALIASES = {
    # food
    "food": "food", "meal": "food", "eat": "food", "eating": "food",
    "lunch": "food", "dinner": "food", "breakfast": "food", "brunch": "food",
    "snack": "food", "cafe": "food", "café": "food", "coffee": "food",
    "restaurant": "food", "drink": "food", "bar": "food", "tea": "food",
    "izakaya": "food", "kissaten": "food",
    # rest
    "rest": "rest", "break": "rest", "relax": "rest", "nap": "rest",
    "downtime": "rest", "free": "rest", "free_time": "rest",
    # travel
    "travel": "travel", "transit": "travel", "transport": "travel",
    "taxi": "travel", "train": "travel", "bus": "travel", "walk": "travel",
    "ferry": "travel", "limo": "travel", "drive": "travel",
    # shop
    "shop": "shop", "shopping": "shop", "market": "shop", "store": "shop",
    "boutique": "shop",
    # hidden / off-beat
    "hidden": "hidden", "local": "hidden", "gem": "hidden", "off-beat": "hidden",
    "neighborhood": "hidden", "alley": "hidden", "underground": "hidden",
}


def _normalize_kind(raw: str | None) -> str:
    if not raw:
        return ""
    s = str(raw).strip().lower().replace(" ", "_")
    if s in _KIND_ALIASES:
        return _KIND_ALIASES[s]
    # the empty string is a perfectly valid "generic anchor"
    return ""


def _normalize_when(raw: str | None) -> str:
    if not raw:
        return "Afternoon"
    s = str(raw).strip().capitalize()
    if s in ("Morning", "Afternoon", "Evening"):
        return s
    low = s.lower()
    if "morn" in low or "am" in low:
        return "Morning"
    if "even" in low or "night" in low or "pm" in low:
        return "Evening"
    return "Afternoon"


def _coerce_int(v) -> int | None:
    if v is None:
        return None
    try:
        return int(v)
    except (TypeError, ValueError):
        return None


def _coerce_day(d: dict, default_day_number: int) -> ItineraryDay:
    slots: list[DaySlot] = []
    for raw in d.get("slots") or []:
        when = _normalize_when(raw.get("when"))
        stops: list[Stop] = []
        for s in raw.get("stops") or []:
            try:
                stops.append(Stop(
                    name=str(s.get("name") or "—"),
                    kind=_normalize_kind(s.get("kind")),
                    meta=str(s.get("meta") or ""),
                    place_id=s.get("place_id") or None,
                    duration_min=_coerce_int(s.get("duration_min")),
                    travel_min_to_next=_coerce_int(s.get("travel_min_to_next")),
                ))
            except Exception as e:
                log.warning("dropping malformed stop %r: %s", s, e)
        slots.append(DaySlot(when=when, stops=stops))

    return ItineraryDay(
        day_number=int(d.get("day_number") or default_day_number),
        title=d.get("title") or f"Day {default_day_number}",
        sub=d.get("sub") or "",
        area=d.get("area"),
        slots=slots,
        why=d.get("why"),
        budget_estimate=d.get("budget_estimate"),
        walking_minutes=d.get("walking_minutes"),
    )


async def plan_trip(
    profile: TravelerProfile, trip: TripDetails
) -> tuple[list[ItineraryDay], ValidationResult, bool]:
    """End-to-end planning pipeline.

    Returns (itinerary, validation, used_fallback).
    """
    persona = profile.persona
    rules = rules_for(persona)

    candidates = await fetch_candidate_places(
        destination=trip.destination,
        experience_types=profile.experience_type or ["culture"],
        persona=persona,
        food_preference=profile.food_pref,
        budget=profile.budget,
    )
    matrix = await estimate_route_matrix(
        candidates, persona, stay_location=trip.stay_location
    )

    raw_days, used_fallback = await generate_itinerary(
        profile=profile.model_dump(),
        persona_rules=rules,
        candidate_places=candidates,
        route_matrix=matrix,
        trip=trip.model_dump(),
    )
    days = [_coerce_day(d, i + 1) for i, d in enumerate(raw_days[: trip.days])]
    validation = validate_itinerary(days, rules, profile)
    return days, validation, used_fallback


# ---------- Replan ---------------------------------------------------------

_DAY_RE = re.compile(r"day\s*(\d)", re.IGNORECASE)


def _deep_clone_days(days: list[ItineraryDay]) -> list[dict]:
    return [d.model_dump(by_alias=True) for d in days]


def _from_dicts(dicts: list[dict]) -> list[ItineraryDay]:
    return [_coerce_day(d, i + 1) for i, d in enumerate(dicts)]


def _add_stop(slot: dict, stop: dict) -> None:
    stop["_added"] = True
    slot["stops"].append(stop)


def _find_slot(day: dict, when: str) -> dict | None:
    for s in day["slots"]:
        if s["when"] == when:
            return s
    return None


def _apply_replan_rules(
    instruction: str, days: list[dict], _persona: str
) -> tuple[list[dict], str, list[int]]:
    """Mirrors data.jsx::applyReplan exactly so the demo is consistent.

    Returns (mutated_days, summary, changed_indices).
    """
    lower = instruction.lower()
    changed: list[int] = []
    summary = ""

    # 1) "more relaxed" / "relax"
    if "more relaxed" in lower or re.search(r"\brelax", lower):
        m = _DAY_RE.search(lower)
        i = int(m.group(1)) - 1 if m else 1
        if 0 <= i < len(days):
            for s in days[i]["slots"]:
                if s["when"] == "Afternoon":
                    _add_stop(s, {"kind": "rest", "name": "Added: 90-min hotel rest", "meta": "New"})
            ev = _find_slot(days[i], "Evening")
            if ev and len(ev["stops"]) > 1:
                ev["stops"][-1]["_removed"] = True
            changed = [i]
            summary = f"Day {i+1} relaxed — rest block added, last evening stop dropped."
        return days, summary, changed

    # 2) hidden gems / off-beat
    if "hidden" in lower or "off-beat" in lower or "off beat" in lower:
        adds = ["Bar Trench", "Ahiru Store natural wine", "SCAI gallery", "Kakimori stationery"]
        for i, d in enumerate(days):
            aft = _find_slot(d, "Afternoon")
            if aft and i < 3:
                _add_stop(aft, {"kind": "hidden", "name": f"Added: {adds[i % len(adds)]}", "meta": "Hidden gem"})
        changed = [0, 1, 2]
        summary = "3 hidden-gem stops added across days 1–3."
        return days, summary, changed

    # 3) reduce walking
    if "reduce walking" in lower or "less walking" in lower or "low walk" in lower:
        for i, d in enumerate(days):
            morn = _find_slot(d, "Morning")
            if morn:
                stop = {"kind": "travel", "name": "Switched: taxi for first transfer", "meta": "Was: walk · ~12 min saved", "_added": True}
                morn["stops"].insert(0, stop)
            if i == 2 and len(d["slots"]) > 1:
                for st in d["slots"][1]["stops"]:
                    if st.get("kind") != "food":
                        st["_removed"] = True
        changed = list(range(len(days)))
        summary = "Walking reduced — taxis swapped in, day 3 trimmed."
        return days, summary, changed

    # 4) cheaper / budget
    if "cheap" in lower or "budget" in lower:
        for i, d in enumerate(days):
            for s in d["slots"]:
                for st in s["stops"]:
                    if "¥¥¥" in (st.get("meta") or ""):
                        st["_removed"] = True
            if len(d["slots"]) > 1:
                _add_stop(d["slots"][1], {"kind": "food", "name": "Added: convenience-store lunch", "meta": "¥ · saves ~¥3000"})
        changed = list(range(len(days)))
        summary = "Top-tier ¥¥¥ restaurants dropped, lighter lunches in."
        return days, summary, changed

    # 5) vegetarian / vegan
    if "vegetarian" in lower or "vegan" in lower:
        for d in days:
            ev = _find_slot(d, "Evening")
            if ev:
                _add_stop(ev, {"kind": "food", "name": "Added: T's Tantan — vegan ramen", "meta": "¥¥ · Tokyo Stn · open till 22:30"})
        changed = list(range(len(days)))
        summary = "Veg-friendly evenings added across all days."
        return days, summary, changed

    # 6) avoid crowds
    if "crowd" in lower or "avoid" in lower:
        for d in days:
            for s in d["slots"]:
                for st in s["stops"]:
                    if re.search(r"shibuya scramble|takeshita|sky tree", st.get("name", ""), re.I):
                        st["_removed"] = True
        changed = [0, 1, 2]
        summary = "Crowded landmarks dropped, quieter alts kept."
        return days, summary, changed

    # 7) shopping
    if "shop" in lower:
        if len(days) > 2:
            aft = _find_slot(days[2], "Afternoon")
            if aft:
                _add_stop(aft, {"kind": "shop", "name": "Added: Kuramae makers shopping", "meta": "2 hrs · paper, leather"})
        if len(days) > 3:
            aft = _find_slot(days[3], "Afternoon")
            if aft:
                _add_stop(aft, {"kind": "shop", "name": "Added: Daikanyama T-Site browsing", "meta": "90 min"})
        changed = [i for i in (2, 3) if i < len(days)]
        summary = "Shopping windows added on days 3 and 4."
        return days, summary, changed

    # 8) free evenings
    if "evening" in lower and "free" in lower:
        for d in days:
            ev = _find_slot(d, "Evening")
            if ev:
                for st in ev["stops"]:
                    st["_removed"] = True
                _add_stop(ev, {"kind": "rest", "name": "Free evening — your call", "meta": "Open block"})
        changed = list(range(len(days)))
        summary = "All evenings cleared — yours to wander."
        return days, summary, changed

    # 9) generic: target mentioned day or day 1
    m = _DAY_RE.search(lower)
    i = int(m.group(1)) - 1 if m else 0
    if 0 <= i < len(days):
        aft = _find_slot(days[i], "Afternoon")
        if aft:
            _add_stop(aft, {"kind": "hidden", "name": f"Adjusted per request: {instruction}", "meta": "AI-generated"})
        changed = [i]
        summary = f'Day {i+1} adjusted per: "{instruction}".'
    return days, summary, changed


async def replan_trip(
    profile: TravelerProfile,
    current_days: list[ItineraryDay],
    instruction: str,
) -> tuple[list[ItineraryDay], str, list[int], ValidationResult]:
    rules = rules_for(profile.persona)
    raw = _deep_clone_days(current_days)
    new_raw, summary, changed = _apply_replan_rules(instruction, raw, profile.persona)
    new_days = _from_dicts(new_raw)
    # Carry day_number/title/sub/area/why from the old days (replan only mutates stops)
    for old, new in zip(current_days, new_days):
        new.title = old.title
        new.sub = old.sub
        new.area = old.area
        new.why = old.why
        new.day_number = old.day_number
        new.walking_minutes = old.walking_minutes
        new.budget_estimate = old.budget_estimate
    validation = validate_itinerary(new_days, rules, profile)
    return new_days, summary, changed, validation
