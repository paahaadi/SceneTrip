"""FastAPI entrypoint for SceneTrip / TripSaathi.

Endpoints (PRD §17):
  GET  /health
  POST /profile/create
  POST /trip/plan
  POST /trip/replan

Sessions are in-process for the MVP. The session_id ties profile → plan →
replan throughout the browser session. (Cloud Run scales to one container
for the demo; horizontal scaling would need a Redis store — out of scope.)
"""
from __future__ import annotations

import logging
import os
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# Auto-load .env from the repo root (one level above backend/) so plain
# `uvicorn app.main:app` picks up GEMINI_API_KEY without manual exports.
load_dotenv(Path(__file__).resolve().parents[1] / ".env")

from .persona_rules import rules_for
from .planner import plan_trip, replan_trip
from .schemas import (
    CreateProfileRequest,
    CreateProfileResponse,
    PlanRequest,
    PlanResponse,
    ReplanRequest,
    ReplanResponse,
    SessionState,
    TravelerProfile,
)


logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
log = logging.getLogger(__name__)


SESSION_TTL_MINUTES = int(os.getenv("SESSION_TTL_MINUTES", "120"))

app = FastAPI(title="SceneTrip · TripSaathi", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "*").split(","),
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---- in-memory session store ---------------------------------------------

_sessions: dict[str, SessionState] = {}
_session_touched_at: dict[str, datetime] = {}


def _gc_sessions() -> None:
    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(minutes=SESSION_TTL_MINUTES)
    expired = [sid for sid, t in _session_touched_at.items() if t < cutoff]
    for sid in expired:
        _sessions.pop(sid, None)
        _session_touched_at.pop(sid, None)


def _touch(sid: str) -> None:
    _session_touched_at[sid] = datetime.now(timezone.utc)


def _get_session(sid: str) -> SessionState:
    _gc_sessions()
    if sid not in _sessions:
        raise HTTPException(status_code=404, detail="session not found or expired")
    _touch(sid)
    return _sessions[sid]


# ---- endpoints ------------------------------------------------------------

@app.get("/health")
async def health() -> dict:
    return {"ok": True, "service": "scenetrip", "version": app.version}


@app.post("/profile/create", response_model=CreateProfileResponse)
async def create_profile(req: CreateProfileRequest) -> CreateProfileResponse:
    """Build a TravelerProfile from chat onboarding answers and assign a session."""
    rules = rules_for(req.persona)

    # Coerce loose answers from chat into the strict TravelerProfile schema.
    raw = req.model_dump()
    profile = TravelerProfile(
        name=raw.get("name") or "Traveler",
        age=int(raw.get("age") or 30),
        gender=raw.get("gender"),
        group_type=raw.get("group") or raw.get("group_type"),
        persona=req.persona,
        pace=raw.get("pace") or "Balanced",
        budget=raw.get("budget") or "Mid-range",
        experience_type=raw.get("experience") or raw.get("experience_type") or [],
        food_pref=raw.get("food") or raw.get("food_pref") or "No preference",
        walking_comfort=raw.get("walk") or raw.get("walking_comfort") or rules["walking_level"].title(),
        mobility_needs=raw.get("access") or raw.get("mobility_needs") or "None",
        safety_pref=raw.get("safety") or raw.get("safety_pref") or "Only at night",
        crowd_pref=raw.get("crowd") or raw.get("crowd_pref") or "Balanced mix",
    )

    sid = uuid.uuid4().hex
    state = SessionState(
        session_id=sid,
        profile=profile,
        persona_summary=rules["persona_summary"],
    )
    _sessions[sid] = state
    _touch(sid)
    log.info("created session %s for persona=%s", sid, profile.persona)

    return CreateProfileResponse(
        session_id=sid,
        profile=profile,
        persona_summary=rules["persona_summary"],
        persona_rules=rules,
    )


@app.post("/trip/plan", response_model=PlanResponse)
async def plan(req: PlanRequest) -> PlanResponse:
    state = _get_session(req.session_id)
    days, validation, used_fallback = await plan_trip(state.profile, req.trip)
    state.trip_details = req.trip
    state.current_itinerary = days
    return PlanResponse(
        session_id=req.session_id,
        itinerary=days,
        validation=validation,
        used_fallback=used_fallback,
    )


@app.post("/trip/replan", response_model=ReplanResponse)
async def replan(req: ReplanRequest) -> ReplanResponse:
    state = _get_session(req.session_id)
    if not state.current_itinerary:
        raise HTTPException(status_code=400, detail="no current itinerary — call /trip/plan first")
    days, summary, changed, validation = await replan_trip(
        state.profile, state.current_itinerary, req.instruction
    )
    state.current_itinerary = days
    state.last_replan_summary = summary
    return ReplanResponse(
        session_id=req.session_id,
        itinerary=days,
        summary=summary,
        changed_days=changed,
        validation=validation,
    )


# convenience for local dev
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8080, reload=True)
