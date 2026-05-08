// Thin client for the FastAPI backend. Vite proxies /api → backend in dev;
// in production set VITE_API_BASE to the deployed Cloud Run URL.

const BASE = import.meta.env.VITE_API_BASE || '/api';

async function jsonPost(path, body) {
  const r = await fetch(`${BASE}${path}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  if (!r.ok) {
    const text = await r.text().catch(() => '');
    throw new Error(`${path} ${r.status}: ${text || r.statusText}`);
  }
  return r.json();
}

export const api = {
  health: () => fetch(`${BASE}/health`).then((r) => r.json()),

  // answers is the full collected onboarding payload — backend is permissive.
  createProfile: (answers) => jsonPost('/profile/create', answers),

  plan: (sessionId, trip) => jsonPost('/trip/plan', { session_id: sessionId, trip }),

  replan: (sessionId, instruction) =>
    jsonPost('/trip/replan', { session_id: sessionId, instruction }),
};

// Map the trip-question chat answers into the strict TripDetails shape.
export function tripDetailsFromAnswers(answers) {
  return {
    destination: answers.destination || 'tokyo',
    dates: answers.dates || null,
    days: parseInt(answers.days || '5', 10),
    total_budget: answers.total_budget || null,
    flights_booked: answers.flights_booked === 'Yes' ? true : answers.flights_booked === 'Not yet' ? false : null,
    stay_booked: answers.stay_booked === 'Yes' ? true : answers.stay_booked === 'Not yet' ? false : null,
    stay_location: null,
    stay_type: answers.stay_type || null,
    area_pref: answers.stay_area || null,
    include_restaurants: answers.restaurants !== 'No',
    include_shopping: answers.shopping !== 'No',
    include_free_time: answers.free_time !== 'No',
  };
}
