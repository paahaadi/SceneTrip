"""Pure-function validator for itineraries against persona rules.

Called on every output of the planner and the replanner. Returns a
ValidationResult listing every constraint violation (warn or error). The API
layer never auto-rewrites — it surfaces issues to the caller and the prompt
loop can react.
"""
from __future__ import annotations

from datetime import time

from .schemas import ItineraryDay, TravelerProfile, ValidationIssue, ValidationResult


# stops with these kinds *don't* count against max_attractions
_NON_ANCHOR_KINDS = {"food", "rest", "travel"}


def _parse_hhmm(s: str) -> time:
    h, m = s.split(":")
    return time(int(h), int(m))


def _count_anchors(day: ItineraryDay) -> int:
    n = 0
    for slot in day.slots:
        for stop in slot.stops:
            if stop.removed:
                continue
            if stop.kind not in _NON_ANCHOR_KINDS:
                n += 1
    return n


def _has_rest_after_lunch(day: ItineraryDay) -> bool:
    aft = next((s for s in day.slots if s.when == "Afternoon"), None)
    if not aft:
        return False
    return any(s.kind == "rest" and not s.removed for s in aft.stops)


def _evening_count(day: ItineraryDay) -> int:
    ev = next((s for s in day.slots if s.when == "Evening"), None)
    if not ev:
        return 0
    return sum(1 for s in ev.stops if not s.removed)


def _has_kw(day: ItineraryDay, keywords: tuple[str, ...]) -> bool:
    text = " ".join(
        f"{stop.name} {stop.meta}".lower()
        for slot in day.slots
        for stop in slot.stops
        if not stop.removed
    )
    return any(k in text for k in keywords)


def validate_itinerary(
    itinerary: list[ItineraryDay],
    rules: dict,
    profile: TravelerProfile,
) -> ValidationResult:
    issues: list[ValidationIssue] = []

    max_anchors = rules.get("max_attractions_per_day")
    walking_level = rules.get("walking_level")
    guardrails = rules.get("guardrails", {})

    for day in itinerary:
        d = day.day_number

        # 1) Anchor count
        if max_anchors is not None:
            anchors = _count_anchors(day)
            if anchors > max_anchors:
                issues.append(ValidationIssue(
                    day_number=d,
                    rule="max_attractions_per_day",
                    severity="error",
                    message=(
                        f"Day {d} has {anchors} anchored attractions; persona "
                        f"allows at most {max_anchors}."
                    ),
                ))

        # 2) Family — mandatory afternoon rest
        if guardrails.get("food_safety_required") and rules.get(
            "mandatory_rest_after_lunch_minutes"
        ):
            if not _has_rest_after_lunch(day):
                issues.append(ValidationIssue(
                    day_number=d,
                    rule="mandatory_rest_after_lunch",
                    severity="warn",
                    message=f"Day {d} is missing the post-lunch rest block.",
                ))

        # 3) Senior — avoid loud nightlife / late evening density
        if guardrails.get("avoid_loud_nightlife_areas"):
            if _has_kw(day, ("nightclub", "roppongi nightlife", "club ", "dive bar")):
                issues.append(ValidationIssue(
                    day_number=d,
                    rule="avoid_loud_nightlife_areas",
                    severity="error",
                    message=f"Day {d} includes a nightlife stop; persona excludes it.",
                ))
            if _evening_count(day) > 1:
                issues.append(ValidationIssue(
                    day_number=d,
                    rule="senior_evening_density",
                    severity="warn",
                    message=f"Day {d} evening has more than one stop after 18:30.",
                ))

        # 4) Off-beat — avoid generic chains and tourist traps
        if guardrails.get("avoid_generic_chain_restaurants"):
            if _has_kw(day, ("starbucks", "mcdonald", "kfc ", "subway sandwich")):
                issues.append(ValidationIssue(
                    day_number=d,
                    rule="avoid_chain_restaurants",
                    severity="warn",
                    message=f"Day {d} includes a generic chain restaurant.",
                ))

        if guardrails.get("avoid_tourist_traps"):
            if _has_kw(day, ("scramble crossing photo", "robot restaurant")):
                issues.append(ValidationIssue(
                    day_number=d,
                    rule="avoid_tourist_traps",
                    severity="warn",
                    message=f"Day {d} leans into a known tourist trap.",
                ))

        # 5) Bleisure — no full-day excursions outside the preferred slots
        if guardrails.get("no_full_day_excursions_on_weekdays"):
            if _has_kw(day, ("hakone day-trip", "full-day excursion", "nikko day")):
                issues.append(ValidationIssue(
                    day_number=d,
                    rule="no_full_day_excursion_weekday",
                    severity="error",
                    message=(
                        f"Day {d} books a full-day excursion; bleisure persona "
                        "forbids these on weekdays."
                    ),
                ))

        # 6) Walking-level vs explicit walking_minutes when present
        if day.walking_minutes is not None:
            cap = rules.get("max_walking_minutes_per_day")
            if cap and day.walking_minutes > cap:
                issues.append(ValidationIssue(
                    day_number=d,
                    rule="max_walking_minutes_per_day",
                    severity="warn" if walking_level == "high" else "error",
                    message=(
                        f"Day {d} walking {day.walking_minutes}m exceeds persona "
                        f"cap of {cap}m."
                    ),
                ))

        # 7) Profile-level food preference must be honored where stated
        if profile.food_pref and profile.food_pref.lower() in {
            "vegetarian",
            "vegan",
            "jain",
            "halal",
        }:
            food_stops = [
                stop
                for slot in day.slots
                for stop in slot.stops
                if stop.kind == "food" and not stop.removed
            ]
            # We can't reliably tell from a name alone whether a place is veg —
            # but if there are food stops we expect at least one veg-aware mention.
            if food_stops and not _has_kw(
                day, ("vegetarian", "vegan", "veg ", "veg-", "veg/", "veggie")
            ):
                issues.append(ValidationIssue(
                    day_number=d,
                    rule="food_pref_alignment",
                    severity="warn",
                    message=(
                        f"Day {d} food stops don't visibly honor the "
                        f"{profile.food_pref} preference."
                    ),
                ))

    ok = not any(i.severity == "error" for i in issues)
    return ValidationResult(ok=ok, issues=issues)
