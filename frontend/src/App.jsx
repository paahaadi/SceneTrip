import { useState } from 'react';
import { Intro } from './components/Intro.jsx';
import { TopBar } from './components/TopBar.jsx';
import { ChatWindow } from './components/ChatWindow.jsx';
import { PersonaCard } from './components/PersonaCard.jsx';
import { Planning } from './components/Planning.jsx';
import { ItineraryCard } from './components/ItineraryCard.jsx';
import { ONBOARDING, TRIP_QS } from './data/scripts.js';
import { api, tripDetailsFromAnswers } from './api/client.js';

// Phase machine:
//   intro → onboarding → persona → trip → planning → itinerary
// Single source of truth for session_id, profile, itinerary, replan state.
export default function App() {
  const [phase, setPhase] = useState('intro');
  const [sessionId, setSessionId] = useState(null);
  const [profile, setProfile] = useState({});
  const [persona, setPersona] = useState('off_beat_explorer');
  const [personaRules, setPersonaRules] = useState(null);
  const [destination, setDestination] = useState('tokyo');
  const [days, setDays] = useState([]);
  const [replanState, setReplanState] = useState(null);
  const [planError, setPlanError] = useState(null);
  const [planRequestDone, setPlanRequestDone] = useState(false);
  const [thinking, setThinking] = useState(false);

  const reset = () => {
    setPhase('intro');
    setSessionId(null);
    setProfile({});
    setDays([]);
    setReplanState(null);
    setPlanError(null);
    setPlanRequestDone(false);
  };

  const onOnboardingDone = async (answers) => {
    setProfile(answers);
    setPersona(answers.persona || 'off_beat_explorer');
    try {
      const res = await api.createProfile(answers);
      setSessionId(res.session_id);
      setProfile(res.profile);
      setPersona(res.profile.persona);
      setPersonaRules(res.persona_rules);
    } catch (err) {
      setPlanError(`Could not reach SceneTrip: ${err.message}`);
    }
    setPhase('persona');
  };

  const onTripDone = async (answers) => {
    const trip = tripDetailsFromAnswers(answers);
    setDestination(trip.destination);
    setProfile((p) => ({ ...p, ...answers }));
    setPhase('planning');
    setPlanRequestDone(false);

    if (!sessionId) {
      setPlanError('Missing session — please restart.');
      return;
    }

    try {
      const res = await api.plan(sessionId, trip);
      setDays(res.itinerary || []);
      setReplanState(null);
      setPlanRequestDone(true);
    } catch (err) {
      setPlanError(`Planner failed: ${err.message}`);
      setPlanRequestDone(true);
    }
  };

  const onPlanComplete = () => {
    if (planError) return; // stay on planning, show error
    setPhase('itinerary');
  };

  const onReplan = async (instruction) => {
    if (!sessionId) return;
    setThinking(true);
    try {
      const res = await api.replan(sessionId, instruction);
      setDays(res.itinerary || []);
      setReplanState({ summary: res.summary, changed: res.changed_days });
    } catch (err) {
      setReplanState({ summary: `Replan failed: ${err.message}`, changed: [] });
    } finally {
      setThinking(false);
    }
  };

  return (
    <div className="st-app" data-density="regular" data-form="desktop">
      <TopBar phase={phase} onReset={reset} />
      <div className="st-phase">
        {phase === 'intro' && <Intro onStart={() => setPhase('onboarding')} />}
        {phase === 'onboarding' && (
          <ChatWindow script={ONBOARDING} profile={profile} onDone={onOnboardingDone} />
        )}
        {phase === 'persona' && (
          <PersonaCard
            profile={profile}
            persona={persona}
            personaRules={personaRules}
            onContinue={() => setPhase('trip')}
          />
        )}
        {phase === 'trip' && (
          <ChatWindow script={TRIP_QS} profile={profile} onDone={onTripDone} />
        )}
        {phase === 'planning' && (
          <>
            <Planning actuallyDone={planRequestDone} onComplete={onPlanComplete} />
            {planError && (
              <div
                style={{
                  padding: '12px var(--pad)',
                  color: 'var(--neon)',
                  fontFamily: 'var(--mono)',
                  fontSize: 12,
                  textAlign: 'center',
                }}
              >
                {planError}
              </div>
            )}
          </>
        )}
        {phase === 'itinerary' && days.length > 0 && (
          <ItineraryCard
            destination={destination}
            persona={persona}
            profile={profile}
            days={days}
            replanState={replanState}
            onReplan={onReplan}
            thinking={thinking}
          />
        )}
      </div>
    </div>
  );
}
