"""Pydantic schemas for SceneTrip / TripSaathi.

Single source of truth shared by the REST layer, planner orchestration, and
the validator. The frontend mirrors these shapes (see frontend/src/data/types.js).
"""
from __future__ import annotations

from typing import Literal, Optional
from pydantic import BaseModel, Field, ConfigDict


PersonaId = Literal[
    "first_time_family",
    "bleisure_professional",
    "off_beat_explorer",
    "senior_couple",
]

DestinationKey = Literal["tokyo", "lisbon", "mexico_city", "kyoto"]


# ---------- Profile ----------------------------------------------------------

class TravelerProfile(BaseModel):
    """The full traveler profile collected during chat onboarding (PRD §7.2)."""
    model_config = ConfigDict(extra="forbid")

    name: str
    age: int
    gender: Optional[str] = None
    group_type: Optional[str] = None
    persona: PersonaId
    pace: Optional[str] = "Balanced"
    budget: Optional[str] = "Mid-range"
    experience_type: list[str] = Field(default_factory=list)
    food_pref: Optional[str] = "No preference"
    walking_comfort: Optional[str] = "Medium"
    mobility_needs: Optional[str] = "None"
    safety_pref: Optional[str] = "Only at night"
    crowd_pref: Optional[str] = "Balanced mix"


class TripDetails(BaseModel):
    model_config = ConfigDict(extra="forbid")

    destination: DestinationKey
    dates: Optional[str] = None
    days: int = 5
    total_budget: Optional[str] = None
    flights_booked: Optional[bool] = None
    stay_booked: Optional[bool] = None
    stay_location: Optional[str] = None
    stay_type: Optional[str] = None
    area_pref: Optional[str] = None
    include_restaurants: bool = True
    include_shopping: bool = True
    include_free_time: bool = True


# ---------- Itinerary --------------------------------------------------------

StopKind = Literal["", "food", "rest", "travel", "shop", "hidden"]


class Stop(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str
    kind: StopKind = ""
    meta: str = ""
    place_id: Optional[str] = None  # populated when sourced from Google Places
    duration_min: Optional[int] = None
    travel_min_to_next: Optional[int] = None
    # diff markers used by the replan flow / UI animations
    added: bool = Field(default=False, alias="_added")
    removed: bool = Field(default=False, alias="_removed")


class DaySlot(BaseModel):
    model_config = ConfigDict(extra="forbid")

    when: Literal["Morning", "Afternoon", "Evening"]
    stops: list[Stop] = Field(default_factory=list)


class ItineraryDay(BaseModel):
    model_config = ConfigDict(extra="forbid")

    day_number: int
    title: str
    sub: str = ""
    area: Optional[str] = None
    slots: list[DaySlot] = Field(default_factory=list)
    why: Optional[str] = None  # "persona_fit_reason" — surfaced in UI
    budget_estimate: Optional[str] = None
    safety_notes: Optional[str] = None
    walking_minutes: Optional[int] = None


# ---------- Session ----------------------------------------------------------

class SessionState(BaseModel):
    session_id: str
    profile: TravelerProfile
    persona_summary: str
    trip_details: Optional[TripDetails] = None
    current_itinerary: Optional[list[ItineraryDay]] = None
    last_replan_summary: Optional[str] = None


# ---------- API request/response -------------------------------------------

class CreateProfileRequest(BaseModel):
    """Free-form by design — the chat onboarding answers map straight in.

    `persona` is required; everything else is best-effort. The backend will
    coerce missing fields with persona-aware defaults rather than reject.
    """
    model_config = ConfigDict(extra="allow")

    name: Optional[str] = None
    age: Optional[int] = None
    persona: PersonaId


class CreateProfileResponse(BaseModel):
    session_id: str
    profile: TravelerProfile
    persona_summary: str
    persona_rules: dict


class PlanRequest(BaseModel):
    session_id: str
    trip: TripDetails


class PlanResponse(BaseModel):
    session_id: str
    itinerary: list[ItineraryDay]
    validation: "ValidationResult"
    used_fallback: bool = False


class ReplanRequest(BaseModel):
    session_id: str
    instruction: str


class ReplanResponse(BaseModel):
    session_id: str
    itinerary: list[ItineraryDay]
    summary: str
    changed_days: list[int]
    validation: "ValidationResult"


# ---------- Validator output -------------------------------------------------

class ValidationIssue(BaseModel):
    day_number: int
    rule: str
    message: str
    severity: Literal["warn", "error"] = "warn"


class ValidationResult(BaseModel):
    ok: bool
    issues: list[ValidationIssue] = Field(default_factory=list)


# Forward-ref resolution
PlanResponse.model_rebuild()
ReplanResponse.model_rebuild()
