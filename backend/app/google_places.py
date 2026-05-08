"""Google Places API wrapper.

Uses the Places API (New) Text Search endpoint when a key is configured;
falls back to a curated stub (so the demo runs offline) when not.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Optional

import httpx


_PLACES_TEXT_URL = "https://places.googleapis.com/v1/places:searchText"
_API_KEY_ENV = "GOOGLE_PLACES_API_KEY"


@dataclass
class PlaceResult:
    name: str
    place_id: str
    rating: Optional[float] = None
    user_ratings_total: Optional[int] = None
    price_level: Optional[int] = None  # 1..4
    types: list[str] = field(default_factory=list)
    vicinity: Optional[str] = None
    lat: Optional[float] = None
    lng: Optional[float] = None
    wheelchair_accessible: Optional[bool] = None


# Persona-aware keyword expansions used to bias Text Search.
_PERSONA_KEYWORDS = {
    "off_beat_explorer": "local hidden gem neighborhood",
    "first_time_family": "family friendly safe popular",
    "bleisure_professional": "wifi cafe quiet workspace",
    "senior_couple": "accessible quiet seated",
}


def _build_query(
    destination: str,
    experience_types: list[str],
    persona: str,
    food_preference: Optional[str],
) -> str:
    bits: list[str] = [destination]
    bits.extend(experience_types or [])
    if food_preference and food_preference.lower() != "no preference":
        bits.append(food_preference)
    if kw := _PERSONA_KEYWORDS.get(persona):
        bits.append(kw)
    return " ".join(bits)


def _persona_filter(p: PlaceResult, persona: str) -> bool:
    """Persona-specific post-filter — see PRD §11."""
    if persona == "off_beat_explorer":
        # filter out the obvious tourist density traps
        if (p.user_ratings_total or 0) > 5000:
            return False
    if persona == "senior_couple" and p.wheelchair_accessible is False:
        return False
    if persona == "bleisure_professional":
        types = {t.lower() for t in p.types}
        # cheap heuristic: cafés / coworking favored over far-flung attractions
        if "amusement_park" in types or "zoo" in types:
            return False
    return True


async def fetch_candidate_places(
    destination: str,
    experience_types: list[str],
    persona: str,
    food_preference: Optional[str],
    budget: Optional[str] = None,
    limit: int = 24,
) -> list[PlaceResult]:
    api_key = os.getenv(_API_KEY_ENV)
    if not api_key:
        return _stub_places(destination, persona)

    query = _build_query(destination, experience_types, persona, food_preference)

    field_mask = ",".join([
        "places.id",
        "places.displayName",
        "places.rating",
        "places.userRatingCount",
        "places.priceLevel",
        "places.types",
        "places.formattedAddress",
        "places.location",
        "places.accessibilityOptions",
    ])
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": api_key,
        "X-Goog-FieldMask": field_mask,
    }
    payload = {"textQuery": query, "pageSize": min(limit, 20)}

    async with httpx.AsyncClient(timeout=12.0) as client:
        r = await client.post(_PLACES_TEXT_URL, json=payload, headers=headers)
        r.raise_for_status()
        data = r.json()

    out: list[PlaceResult] = []
    for p in data.get("places", []):
        loc = p.get("location") or {}
        access = p.get("accessibilityOptions") or {}
        out.append(PlaceResult(
            name=(p.get("displayName") or {}).get("text", ""),
            place_id=p.get("id", ""),
            rating=p.get("rating"),
            user_ratings_total=p.get("userRatingCount"),
            price_level=_priceLevelInt(p.get("priceLevel")),
            types=p.get("types") or [],
            vicinity=p.get("formattedAddress"),
            lat=loc.get("latitude"),
            lng=loc.get("longitude"),
            wheelchair_accessible=access.get("wheelchairAccessibleEntrance"),
        ))

    return [p for p in out if _persona_filter(p, persona)]


def _priceLevelInt(s) -> Optional[int]:
    """The new Places API returns 'PRICE_LEVEL_MODERATE' etc; map to 1..4."""
    if not s:
        return None
    table = {
        "PRICE_LEVEL_FREE": 0,
        "PRICE_LEVEL_INEXPENSIVE": 1,
        "PRICE_LEVEL_MODERATE": 2,
        "PRICE_LEVEL_EXPENSIVE": 3,
        "PRICE_LEVEL_VERY_EXPENSIVE": 4,
    }
    if isinstance(s, int):
        return s
    return table.get(s)


# ---------------------------------------------------------------------------
# Offline fallback — keeps the demo working without an API key.

def _stub_places(destination: str, persona: str) -> list[PlaceResult]:
    """Hand-curated places for Tokyo (and a small Lisbon set) used when no
    GOOGLE_PLACES_API_KEY is set. Names match the prototype's seed data so
    the planner output remains coherent."""
    if destination.lower().startswith("tokyo") or destination == "tokyo":
        return [
            PlaceResult(name="Senso-ji Temple", place_id="stub_sensoji",
                        rating=4.5, user_ratings_total=72000, types=["tourist_attraction"],
                        vicinity="Asakusa, Tokyo", lat=35.7148, lng=139.7967),
            PlaceResult(name="Yanaka Ginza", place_id="stub_yanakaginza",
                        rating=4.4, user_ratings_total=2100, types=["shopping_street"],
                        vicinity="Yanaka, Taito", lat=35.7274, lng=139.7649),
            PlaceResult(name="SCAI The Bathhouse", place_id="stub_scai",
                        rating=4.3, user_ratings_total=480, types=["art_gallery"],
                        vicinity="Yanaka, Taito", lat=35.7227, lng=139.7686),
            PlaceResult(name="Shimokitazawa", place_id="stub_shimokita",
                        rating=4.5, user_ratings_total=4900, types=["neighborhood"],
                        vicinity="Setagaya, Tokyo", lat=35.6614, lng=139.6677),
            PlaceResult(name="Kuramae makers walk", place_id="stub_kuramae",
                        rating=4.4, user_ratings_total=1200, types=["neighborhood"],
                        vicinity="Kuramae, Taito", lat=35.7066, lng=139.7912),
            PlaceResult(name="Tsutaya T-Site Daikanyama", place_id="stub_tsutaya",
                        rating=4.4, user_ratings_total=4800, types=["book_store"],
                        vicinity="Daikanyama, Shibuya", lat=35.6504, lng=139.7026),
            PlaceResult(name="teamLab Planets", place_id="stub_teamlab",
                        rating=4.6, user_ratings_total=24000, price_level=3,
                        types=["museum"], vicinity="Toyosu", lat=35.6498, lng=139.7900),
            PlaceResult(name="Ueno Zoo", place_id="stub_uenozoo",
                        rating=4.2, user_ratings_total=18000, price_level=1,
                        types=["zoo"], vicinity="Ueno, Taito", lat=35.7166, lng=139.7714,
                        wheelchair_accessible=True),
            PlaceResult(name="Hamarikyu Garden", place_id="stub_hamarikyu",
                        rating=4.5, user_ratings_total=8400, price_level=1,
                        types=["park"], vicinity="Chuo, Tokyo", lat=35.6597, lng=139.7637,
                        wheelchair_accessible=True),
            PlaceResult(name="Tokyo National Museum", place_id="stub_tnm",
                        rating=4.5, user_ratings_total=11000, price_level=2,
                        types=["museum"], vicinity="Ueno, Tokyo", lat=35.7188, lng=139.7766,
                        wheelchair_accessible=True),
            PlaceResult(name="Blue Bottle Shinjuku", place_id="stub_bluebottle",
                        rating=4.3, user_ratings_total=900, price_level=2,
                        types=["cafe"], vicinity="Shinjuku", lat=35.6938, lng=139.7034),
            PlaceResult(name="Mori Tower observation", place_id="stub_moritower",
                        rating=4.4, user_ratings_total=15000, price_level=3,
                        types=["tourist_attraction"], vicinity="Roppongi", lat=35.6604, lng=139.7292),
            PlaceResult(name="T's Tantan vegan ramen", place_id="stub_tstantan",
                        rating=4.2, user_ratings_total=3200, price_level=2,
                        types=["restaurant"], vicinity="Tokyo Station"),
        ]
    if destination.lower().startswith("lisbon"):
        return [
            PlaceResult(name="Castelo S. Jorge", place_id="stub_castelo", rating=4.5,
                        user_ratings_total=42000, price_level=2, types=["tourist_attraction"]),
            PlaceResult(name="Manteigaria Pastéis", place_id="stub_manteigaria",
                        rating=4.7, user_ratings_total=25000, price_level=1, types=["bakery"]),
            PlaceResult(name="LX Factory", place_id="stub_lx", rating=4.4,
                        user_ratings_total=18000, types=["shopping_mall"]),
        ]
    return []
