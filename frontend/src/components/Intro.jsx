export function Intro({ onStart }) {
  return (
    <div className="intro">
      <div className="eyebrow">SceneTrip · v0.1 · Tokyo demo</div>
      <h1>
        AI-planned trips that <em>match your scene.</em>
      </h1>
      <p>
        Tell SceneTrip who's traveling. We assign a persona, build a profile, and
        plan with rules — not vibes. Hidden-gem walks for the off-beat. Rest
        blocks for the family. No full-day excursions on a working Tuesday.
      </p>
      <div className="actions">
        <button className="btn primary" onClick={onStart}>Start the conversation →</button>
        <span className="kbd" style={{ alignSelf: 'center' }}>
          ~ 90 seconds · session-only · no signup
        </span>
      </div>
    </div>
  );
}
