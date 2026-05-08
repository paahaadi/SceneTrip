const PHASES = ['onboarding', 'persona', 'trip', 'planning', 'itinerary'];

export function TopBar({ phase, onReset }) {
  const cur = PHASES.indexOf(phase);
  return (
    <div className="st-top">
      <div className="st-logo">
        <div className="mark">S</div>
        <div className="name">
          Scene<em>Trip</em>
        </div>
      </div>
      <div className="st-progress" aria-label="progress">
        {PHASES.map((p, i) => (
          <span key={p} data-on={i < cur ? 1 : i === cur ? 2 : 0} />
        ))}
      </div>
      <button
        className="btn ghost icon"
        onClick={onReset}
        title="Restart"
        style={{
          padding: '6px 10px',
          fontSize: 11,
          fontFamily: 'var(--mono)',
          letterSpacing: '0.06em',
          textTransform: 'uppercase',
          color: 'var(--ink-3)',
        }}
      >
        ↺ Restart
      </button>
    </div>
  );
}
