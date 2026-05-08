"""Persona rule engine.

These rules are *hard constraints* that drive both the Gemini prompt and the
validator. Wording lifted from the PRD and the prototype's persona reveal
copy so the UI rationale matches what the engine actually enforces.
"""
from __future__ import annotations

from typing import Any


PERSONA_RULES: dict[str, dict[str, Any]] = {
    "first_time_family": {
        "id": "first_time_family",
        "display_name": "First-Time Family",
        "tag": "Family",
        "eyebrow": "Persona · 01",
        "max_attractions_per_day": 3,
        "day_start": "10:00",
        "day_end": "20:00",
        "mandatory_rest_after_lunch_minutes": 90,
        "walking_level": "medium",
        "max_walking_minutes_per_day": 120,
        "guardrails": {
            "avoid_late_night": True,
            "food_safety_required": True,
            "avoid_unrated_street_food": True,
            "stroller_friendly_routes": True,
        },
        "ui_rules": [
            "Max 3 attractions per day",
            "Day window: 10:00 → 20:00",
            "90-min rest block after lunch",
            "Walking comfort: medium",
            "Food safety required, avoid late-night",
        ],
        "persona_summary": (
            "Comfort, safety and predictability come first. SceneTrip will keep days "
            "light, food family-friendly, and bake in proper rest after lunch."
        ),
    },
    "bleisure_professional": {
        "id": "bleisure_professional",
        "display_name": "Bleisure Professional",
        "tag": "Bleisure",
        "eyebrow": "Persona · 02",
        "max_attractions_per_day": 2,
        "preferred_slots": ["07:00-09:00", "17:30-22:00"],
        "walking_level": "medium",
        "max_walking_minutes_per_day": 100,
        "guardrails": {
            "no_full_day_excursions_on_weekdays": True,
            "require_high_speed_connectivity": True,
            "compact_routing": True,
        },
        "ui_rules": [
            "Max 2 stops per day",
            "Slots: 07:00–09:00 · 17:30–22:00",
            "No full-day excursions on weekdays",
            "Reliable Wi-Fi cafés prioritised",
            "Compact, punctual routing",
        ],
        "persona_summary": (
            "Work first, scene second. SceneTrip plans tight morning and evening "
            "windows, keeps routes efficient, and never books a full-day excursion "
            "mid-week."
        ),
    },
    "off_beat_explorer": {
        "id": "off_beat_explorer",
        "display_name": "Off-Beat Explorer",
        "tag": "Off-Beat",
        "eyebrow": "Persona · 03",
        "max_attractions_per_day": 2,
        "day_start": "06:00",
        "day_end": "19:00",
        "walking_level": "high",
        "max_walking_minutes_per_day": 240,
        "guardrails": {
            "avoid_tourist_traps": True,
            "avoid_generic_chain_restaurants": True,
            "lean_neighborhood_and_market_led": True,
        },
        "ui_rules": [
            "Max 2 anchored attractions per day",
            "Day window: 06:00 → 19:00 (early starts ok)",
            "Walking comfort: high",
            "Avoid tourist traps & chain restaurants",
            "Lean cultural, neighborhood, market-led",
        ],
        "persona_summary": (
            "You skip the queue and find the alley. SceneTrip will plan fewer, deeper "
            "stops, lean into local neighborhoods, hidden corners and unique food, and "
            "avoid generic tourist traps."
        ),
    },
    "senior_couple": {
        "id": "senior_couple",
        "display_name": "Senior Couple",
        "tag": "Senior",
        "eyebrow": "Persona · 04",
        "max_attractions_per_day": 2,
        "day_start": "10:30",
        "day_end": "18:30",
        "walking_level": "low",
        "max_walking_minutes_per_day": 60,
        "guardrails": {
            "avoid_steep_climbs": True,
            "avoid_long_queues": True,
            "avoid_loud_nightlife_areas": True,
            "prefer_accessible": True,
        },
        "ui_rules": [
            "Max 2 attractions per day",
            "Day window: 10:30 → 18:30",
            "Walking comfort: low",
            "Avoid steep climbs, long queues",
            "No loud nightlife districts",
        ],
        "persona_summary": (
            "Slower, calmer, kinder on the legs. SceneTrip plans 1–2 anchor activities "
            "a day, low walking, accessible places and shorter transfers."
        ),
    },
}


def rules_for(persona: str) -> dict[str, Any]:
    if persona not in PERSONA_RULES:
        raise ValueError(f"Unknown persona: {persona}")
    return PERSONA_RULES[persona]


def persona_summary(persona: str) -> str:
    return rules_for(persona)["persona_summary"]
