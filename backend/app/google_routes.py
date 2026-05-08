"""Google Routes API wrapper — sequential travel-time matrix.

Computes a simple distance/time matrix between an ordered list of places. We
use the Routes API ComputeRouteMatrix endpoint when a key is present and a
heuristic estimate otherwise. The persona drives which travel mode we ask
for.
"""
from __future__ import annotations

import math
import os
from dataclasses import dataclass, field
from typing import Optional

import httpx

from .google_places import PlaceResult


_ROUTE_MATRIX_URL = "https://routes.googleapis.com/distanceMatrix/v2:computeRouteMatrix"
_API_KEY_ENV = "GOOGLE_ROUTES_API_KEY"


@dataclass
class Leg:
    from_idx: int
    to_idx: int
    duration_min: int
    distance_m: int


@dataclass
class RouteMatrix:
    mode: str
    legs: list[Leg] = field(default_factory=list)
    total_walking_minutes: int = 0
    flagged_overruns: list[int] = field(default_factory=list)


_PERSONA_MODE = {
    "off_beat_explorer": "WALK",
    "first_time_family": "TRANSIT",
    "bleisure_professional": "TRANSIT",
    "senior_couple": "DRIVE",  # taxi-anchored
}

# walking caps that line up with persona_rules.max_walking_minutes_per_day
_WALKING_LEG_FLAG_MIN = {
    "off_beat_explorer": 60,
    "first_time_family": 25,
    "bleisure_professional": 25,
    "senior_couple": 12,
}


def _haversine_m(a: PlaceResult, b: PlaceResult) -> float:
    if None in (a.lat, a.lng, b.lat, b.lng):
        return 1500.0  # neutral default
    R = 6371000.0
    p1, p2 = math.radians(a.lat), math.radians(b.lat)
    dp = math.radians(b.lat - a.lat)
    dl = math.radians(b.lng - a.lng)
    h = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * R * math.asin(math.sqrt(h))


def _heuristic_duration_min(distance_m: float, mode: str) -> int:
    speeds = {"WALK": 4.5, "TRANSIT": 22.0, "DRIVE": 30.0}  # km/h
    kmh = speeds.get(mode, 5.0)
    return max(1, int(round((distance_m / 1000.0) / kmh * 60.0)))


async def estimate_route_matrix(
    places: list[PlaceResult],
    persona: str,
    stay_location: Optional[str] = None,
) -> RouteMatrix:
    if not places:
        return RouteMatrix(mode="WALK")

    mode = _PERSONA_MODE.get(persona, "TRANSIT")
    api_key = os.getenv(_API_KEY_ENV)

    legs: list[Leg] = []

    if api_key and all(p.lat is not None and p.lng is not None for p in places):
        legs = await _legs_via_api(places, mode, api_key)
    else:
        legs = _legs_via_heuristic(places, mode)

    flag_cap = _WALKING_LEG_FLAG_MIN.get(persona, 30) if mode == "WALK" else 999
    flagged = [i for i, leg in enumerate(legs) if leg.duration_min > flag_cap]
    walking_total = sum(l.duration_min for l in legs) if mode == "WALK" else 0

    return RouteMatrix(
        mode=mode,
        legs=legs,
        total_walking_minutes=walking_total,
        flagged_overruns=flagged,
    )


def _legs_via_heuristic(places: list[PlaceResult], mode: str) -> list[Leg]:
    legs: list[Leg] = []
    for i in range(len(places) - 1):
        d = _haversine_m(places[i], places[i + 1])
        legs.append(Leg(
            from_idx=i,
            to_idx=i + 1,
            duration_min=_heuristic_duration_min(d, mode),
            distance_m=int(d),
        ))
    return legs


async def _legs_via_api(
    places: list[PlaceResult], mode: str, api_key: str
) -> list[Leg]:
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": api_key,
        "X-Goog-FieldMask": (
            "originIndex,destinationIndex,duration,distanceMeters,condition"
        ),
    }
    waypoints = [
        {"waypoint": {"location": {"latLng": {"latitude": p.lat, "longitude": p.lng}}}}
        for p in places
    ]
    payload = {"origins": waypoints, "destinations": waypoints, "travelMode": mode}

    legs: list[Leg] = []
    async with httpx.AsyncClient(timeout=15.0) as client:
        r = await client.post(_ROUTE_MATRIX_URL, json=payload, headers=headers)
        r.raise_for_status()
        # Routes API returns a stream of JSON objects when called with HTTP;
        # in practice the v2 endpoint returns a JSON array.
        data = r.json() if r.headers.get("content-type", "").startswith("application/json") else []
        for cell in data:
            origin = cell.get("originIndex")
            dest = cell.get("destinationIndex")
            if origin is None or dest is None or origin == dest:
                continue
            if dest != origin + 1:  # we only care about sequential legs
                continue
            dur_s = cell.get("duration", "0s")
            dur = int(str(dur_s).rstrip("s") or 0) // 60
            dist = int(cell.get("distanceMeters", 0))
            legs.append(Leg(from_idx=origin, to_idx=dest, duration_min=max(1, dur), distance_m=dist))

    if not legs:  # API responded but didn't give us sequential legs — fall back
        legs = _legs_via_heuristic(places, mode)
    return legs
