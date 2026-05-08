import { PERSONAS } from '../data/personas.js';

// The mirror moment — first delight beat after onboarding. Persona display
// data is local, but the rules list comes from the backend response so it
// matches whatever persona_rules.py currently encodes.
export function PersonaCard({ profile, persona, personaRules, onContinue }) {
  const p = PERSONAS[persona];
  const rules = personaRules?.ui_rules || p.rules;
  const desc = personaRules?.persona_summary || p.desc;

  return (
    <div className="persona-wrap">
      <div className="persona-card">
        <div className="stamp">// session.persona</div>
        <div className="eyebrow">{p.eyebrow} · Profile assigned</div>
        <h1>
          {profile.name || 'Your'}<em>'s</em> travel scene.
        </h1>
        <div className="desc">{desc}</div>
        <div className="persona-grid">
          <div className="pg-cell"><div className="k">Persona</div><div className="v">{p.name}</div></div>
          <div className="pg-cell"><div className="k">Pace</div><div className="v">{profile.pace || p.pace}</div></div>
          <div className="pg-cell"><div className="k">Budget</div><div className="v">{profile.budget || 'Mid-range'}</div></div>
          <div className="pg-cell"><div className="k">Food</div><div className="v">{profile.food_pref || profile.food || 'No preference'}</div></div>
          <div className="pg-cell"><div className="k">Walking</div><div className="v">{profile.walking_comfort || profile.walk || p.walking}</div></div>
          <div className="pg-cell">
            <div className="k">Mood</div>
            <div className="v">
              {(profile.experience_type || profile.experience || ['Hidden gems']).slice(0, 3).join(' · ')}
            </div>
          </div>
        </div>
      </div>

      <div className="rules-card">
        <h3>// rules engine — applied constraints</h3>
        <div className="rules-list">
          {rules.map((r, i) => (
            <div className="rule-row" key={i}>
              <div className="bullet" />
              <div>{r}</div>
            </div>
          ))}
        </div>
      </div>

      <div
        style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          gap: 10,
          paddingBottom: 12,
          flexWrap: 'wrap',
        }}
      >
        <div
          style={{
            fontFamily: 'var(--mono)',
            fontSize: 11,
            color: 'var(--ink-3)',
            letterSpacing: '0.04em',
          }}
        >
          {p.followup}
        </div>
        <button className="btn primary" onClick={onContinue} style={{ flex: '0 0 auto' }}>
          Plan my trip →
        </button>
      </div>
    </div>
  );
}
