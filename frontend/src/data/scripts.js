// Onboarding + trip-question scripts. The chat phase is a state machine
// (PRD §7.2): one question at a time, follow-ups computed from earlier
// answers. The bot never asks the same question twice within a session.

export const ONBOARDING = [
  { id: 'intro', kind: 'note', text: "Hi, I'm SceneTrip — your AI travel planner. Before I plan your trip, I'll quickly understand your travel style so the itinerary actually matches your scene." },
  { id: 'name', kind: 'text', q: "First — what should I call you?", placeholder: 'Your name', default: 'Aditya' },
  { id: 'age', kind: 'text', q: "And how old are you, {name}?", placeholder: 'Age', default: '29', inputType: 'number' },
  { id: 'gender', kind: 'chip', q: "Gender? (optional)", options: ['Female', 'Male', 'Non-binary', 'Prefer not to say'], default: 'Prefer not to say' },
  { id: 'group', kind: 'chip', q: "Who are you traveling with?", options: ['Solo', 'Couple', 'Family', 'Friends', 'Group'], default: 'Solo' },
  {
    id: 'persona', kind: 'chip-rich', q: "Which traveler type sounds most like you?",
    options: [
      { v: 'first_time_family', label: 'First-Time Family', sub: 'Comfort, safety, family-friendly' },
      { v: 'bleisure_professional', label: 'Bleisure Professional', sub: 'Work-trip with off-hours' },
      { v: 'off_beat_explorer', label: 'Off-Beat Explorer', sub: 'Local, hidden, immersive' },
      { v: 'senior_couple', label: 'Senior Couple', sub: 'Slower, calm, accessible' },
    ],
    default: 'off_beat_explorer'
  },
  { id: 'pace', kind: 'chip', q: "What's your travel pace?", options: ['Relaxed', 'Balanced', 'Packed'], default: 'Balanced' },
  { id: 'budget', kind: 'chip', q: "And budget preference?", options: ['Budget', 'Mid-range', 'Premium', 'Luxury'], default: 'Mid-range' },
  {
    id: 'experience', kind: 'chip-multi', q: "What kind of experience do you want most? (pick a few)",
    options: ['Adventure', 'Culture', 'Food', 'Nature', 'Shopping', 'Wellness', 'Nightlife', 'Spiritual', 'Hidden gems', 'Mixed'],
    default: ['Hidden gems', 'Culture', 'Food']
  },
  { id: 'food', kind: 'chip', q: "Food preference?", options: ['Vegetarian', 'Vegan', 'Jain', 'Halal', 'Non-vegetarian', 'No preference'], default: 'Vegetarian' },
  { id: 'walk', kind: 'chip', q: "How much walking are you comfortable with per day?", options: ['Low', 'Medium', 'High'], default: 'High' },
  { id: 'access', kind: 'chip', q: "Any mobility or accessibility needs?", options: ['None', 'Yes — limited stairs', 'Yes — wheelchair', 'Other'], default: 'None' },
  { id: 'safety', kind: 'chip', q: "Should SceneTrip prioritize extra-safe areas and transport?", options: ['Yes', 'No', 'Only at night'], default: 'Only at night' },
  { id: 'crowd', kind: 'chip', q: "Popular highlights or hidden gems?", options: ['Popular highlights', 'Local hidden gems', 'Balanced mix'], default: 'Local hidden gems' },
];

export const TRIP_QS = [
  {
    id: 'destination', kind: 'chip-rich', q: "Beautiful. Where do you want to go?",
    options: [
      { v: 'tokyo', label: 'Tokyo, Japan', sub: '5 days suggested' },
      { v: 'lisbon', label: 'Lisbon, Portugal', sub: '4 days suggested' },
      { v: 'mexico_city', label: 'Mexico City', sub: '5 days suggested' },
      { v: 'kyoto', label: 'Kyoto, Japan', sub: '4 days suggested' },
    ],
    default: 'tokyo'
  },
  { id: 'dates', kind: 'chip', q: "When are you going?", options: ['This weekend', 'Next month', 'In 2-3 months', 'Flexible'], default: 'Next month' },
  { id: 'days', kind: 'chip', q: "How many days?", options: ['3', '4', '5', '7', '10'], default: '5' },
  { id: 'total_budget', kind: 'chip', q: "Approximate total budget?", options: ['Under $1k', '$1-2k', '$2-4k', '$4k+'], default: '$2-4k' },
  { id: 'flights_booked', kind: 'chip', q: "Have you booked flights?", options: ['Yes', 'Not yet'], default: 'Yes' },
  { id: 'stay_booked', kind: 'chip', q: "And your stay?", options: ['Yes', 'Not yet'], default: 'Yes' },
  { id: 'stay_area', kind: 'chip', q: "What area is your stay in (or preferred)?", options: ['City center', 'Near nature', 'Quiet residential', 'Near nightlife', 'Near airport/station'], default: 'City center' },
  { id: 'stay_type', kind: 'chip', q: "Stay type?", options: ['Hotel', 'Boutique stay', 'Airbnb / apartment', 'Hostel', 'Resort', 'Luxury'], default: 'Boutique stay' },
  { id: 'restaurants', kind: 'chip', q: "Want restaurants included in the daily plan?", options: ['Yes', 'No'], default: 'Yes' },
  { id: 'shopping', kind: 'chip', q: "Include shopping / market time?", options: ['Yes', 'A little', 'No'], default: 'A little' },
  { id: 'free_time', kind: 'chip', q: "Leave free time each day?", options: ['Yes', 'No'], default: 'Yes' },
];
