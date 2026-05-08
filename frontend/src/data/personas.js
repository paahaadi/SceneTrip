// Display copy + UI metadata for the four personas. The hard rules are
// owned by the backend (persona_rules.py); these strings exist for the
// PersonaCard reveal and the persona-fit narrative in the UI.

export const PERSONAS = {
  off_beat_explorer: {
    id: 'off_beat_explorer',
    name: 'Off-Beat Explorer',
    eyebrow: 'Persona · 03',
    tag: 'Off-Beat',
    desc: "You skip the queue and find the alley. SceneTrip will plan fewer, deeper stops, lean into local neighborhoods, hidden corners and unique food, and avoid generic tourist traps.",
    rules: [
      'Max 2 anchored attractions per day',
      'Day window: 06:00 → 19:00 (early starts ok)',
      'Walking comfort: high',
      'Avoid tourist traps & chain restaurants',
      'Lean cultural, neighborhood, market-led',
    ],
    walking: 'High',
    pace: 'Balanced',
    followup: 'Should I avoid mainstream tourist spots and focus on local neighborhoods, hidden gems, and unique food stops?',
  },
  first_time_family: {
    id: 'first_time_family',
    name: 'First-Time Family',
    eyebrow: 'Persona · 01',
    tag: 'Family',
    desc: 'Comfort, safety and predictability come first. SceneTrip will keep days light, food family-friendly, and bake in proper rest after lunch.',
    rules: [
      'Max 3 attractions per day',
      'Day window: 10:00 → 20:00',
      '90-min rest block after lunch',
      'Walking comfort: medium',
      'Food safety required, avoid late-night',
    ],
    walking: 'Medium',
    pace: 'Relaxed',
    followup: 'Want kid-friendly attractions, safer food options, and a rest break baked into each afternoon?',
  },
  bleisure_professional: {
    id: 'bleisure_professional',
    name: 'Bleisure Professional',
    eyebrow: 'Persona · 02',
    tag: 'Bleisure',
    desc: 'Work first, scene second. SceneTrip plans tight morning and evening windows, keeps routes efficient, and never books a full-day excursion mid-week.',
    rules: [
      'Max 2 stops per day',
      'Slots: 07:00–09:00 · 17:30–22:00',
      'No full-day excursions on weekdays',
      'Reliable Wi-Fi cafés prioritised',
      'Compact, punctual routing',
    ],
    walking: 'Medium',
    pace: 'Packed',
    followup: 'Plan only around your free hours before and after work? I can also flag cafés with reliable Wi-Fi.',
  },
  senior_couple: {
    id: 'senior_couple',
    name: 'Senior Couple',
    eyebrow: 'Persona · 04',
    tag: 'Senior',
    desc: 'Slower, calmer, kinder on the legs. SceneTrip plans 1–2 anchor activities a day, low walking, accessible places and shorter transfers.',
    rules: [
      'Max 2 attractions per day',
      'Day window: 10:30 → 18:30',
      'Walking comfort: low',
      'Avoid steep climbs, long queues',
      'No loud nightlife districts',
    ],
    walking: 'Low',
    pace: 'Relaxed',
    followup: 'Prioritise low-walking, calm and accessible places with shorter transfers?',
  },
};

export const DESTINATIONS = {
  tokyo: { label: 'Tokyo, Japan', sub: '5 days · April 18 – 22' },
  lisbon: { label: 'Lisbon, Portugal', sub: '4 days · May 10 – 13' },
  mexico_city: { label: 'Mexico City', sub: '5 days · June 6 – 10' },
  kyoto: { label: 'Kyoto, Japan', sub: '4 days · April 20 – 23' },
};

// Stylized Tokyo map (relative coordinates, 0–100). Used by MapPane.
export const TOKYO_MAP_AREAS = [
  { id: 'shibuya',    name: 'Shibuya',    x: 30, y: 60 },
  { id: 'shinjuku',   name: 'Shinjuku',   x: 32, y: 42 },
  { id: 'harajuku',   name: 'Harajuku',   x: 35, y: 54 },
  { id: 'ginza',      name: 'Ginza',      x: 60, y: 62 },
  { id: 'asakusa',    name: 'Asakusa',    x: 74, y: 34 },
  { id: 'yanaka',     name: 'Yanaka',     x: 64, y: 30 },
  { id: 'tsukiji',    name: 'Tsukiji',    x: 64, y: 68 },
  { id: 'akihabara',  name: 'Akihabara',  x: 60, y: 46 },
  { id: 'ueno',       name: 'Ueno',       x: 62, y: 36 },
  { id: 'roppongi',   name: 'Roppongi',   x: 42, y: 64 },
  { id: 'odaiba',     name: 'Odaiba',     x: 78, y: 82 },
  { id: 'nakameguro', name: 'Nakameguro', x: 34, y: 70 },
];

export const REPLAN_CHIPS = [
  'Make day 2 more relaxed',
  'Add more hidden gems',
  'Reduce walking',
  'Make it cheaper',
  'Add vegetarian restaurants',
  'Avoid crowded places',
  'Add shopping time',
  'Keep evenings free',
];
