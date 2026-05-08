import { TOKYO_MAP_AREAS, DESTINATIONS } from '../data/personas.js';

// Stylized SVG map of Tokyo. Other destinations show a placeholder until
// per-city map data is added.
export function MapPane({ destinationKey, days, activeDay }) {
  const dest = DESTINATIONS[destinationKey];
  const areas = destinationKey === 'tokyo' ? TOKYO_MAP_AREAS : [];

  if (!areas.length) {
    return (
      <div className="map-pane" style={{ display: 'grid', placeItems: 'center', padding: 24 }}>
        <div style={{ fontFamily: 'var(--mono)', fontSize: 11, color: 'var(--ink-3)', textAlign: 'center' }}>
          Map preview coming soon for {dest?.label || destinationKey}
        </div>
      </div>
    );
  }

  const allAreasOnRoute = days.map((d) => d.area).filter(Boolean);
  const todayArea = days[activeDay]?.area;
  const allPts = allAreasOnRoute
    .map((a) => areas.find((x) => x.id === a))
    .filter(Boolean);
  const todayPt = areas.find((a) => a.id === todayArea);

  const smoothPath = (pts) => {
    if (!pts.length) return '';
    if (pts.length === 1) return `M ${pts[0].x} ${pts[0].y}`;
    let d = `M ${pts[0].x} ${pts[0].y}`;
    for (let i = 0; i < pts.length - 1; i++) {
      const p0 = pts[i - 1] || pts[i];
      const p1 = pts[i];
      const p2 = pts[i + 1];
      const p3 = pts[i + 2] || p2;
      const c1x = p1.x + (p2.x - p0.x) / 6;
      const c1y = p1.y + (p2.y - p0.y) / 6;
      const c2x = p2.x - (p3.x - p1.x) / 6;
      const c2y = p2.y - (p3.y - p1.y) / 6;
      d += ` C ${c1x.toFixed(2)} ${c1y.toFixed(2)}, ${c2x.toFixed(2)} ${c2y.toFixed(2)}, ${p2.x} ${p2.y}`;
    }
    return d;
  };

  const routeKey = allPts.map((p) => p.x + ',' + p.y).join('|') + '·' + activeDay;

  return (
    <div className="map-pane">
      <svg className="map-svg" viewBox="0 0 100 100" preserveAspectRatio="xMidYMid slice" key={routeKey}>
        <defs>
          <pattern id="grid" width="5" height="5" patternUnits="userSpaceOnUse">
            <path d="M 5 0 L 0 0 0 5" fill="none" stroke="rgba(58,46,30,0.05)" strokeWidth="0.15" />
          </pattern>
          <radialGradient id="glow" cx="50%" cy="50%" r="50%">
            <stop offset="0%" stopColor="#b86b3a" stopOpacity="0.32" />
            <stop offset="100%" stopColor="#b86b3a" stopOpacity="0" />
          </radialGradient>
          <linearGradient id="routegrad" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0%" stopColor="#b86b3a" stopOpacity="0.95" />
            <stop offset="100%" stopColor="#5e7e8c" stopOpacity="0.85" />
          </linearGradient>
          <linearGradient id="bayfill" x1="0" x2="0" y1="0" y2="1">
            <stop offset="0%" stopColor="#cfe1e8" stopOpacity="0.55" />
            <stop offset="100%" stopColor="#bcd1da" stopOpacity="0.7" />
          </linearGradient>
          <linearGradient id="parkfill" x1="0" x2="0" y1="0" y2="1">
            <stop offset="0%" stopColor="#cfdcc6" stopOpacity="0.6" />
            <stop offset="100%" stopColor="#bccdb1" stopOpacity="0.7" />
          </linearGradient>
        </defs>
        <rect width="100" height="100" fill="url(#grid)" />

        <path
          d="M 0 88 Q 28 78 52 84 T 100 76 L 100 100 L 0 100 Z"
          fill="url(#bayfill)"
          stroke="rgba(94,126,140,0.35)"
          strokeWidth="0.25"
        />
        <path
          d="M 48 -2 Q 56 28 62 48 T 70 102"
          fill="none"
          stroke="rgba(94,126,140,0.45)"
          strokeWidth="0.7"
          strokeLinecap="round"
        />
        <ellipse cx="35" cy="50" rx="6" ry="3.5" fill="url(#parkfill)" />
        <ellipse cx="63" cy="35" rx="4" ry="2.6" fill="url(#parkfill)" />
        <ellipse cx="14" cy="80" rx="5" ry="3" fill="url(#parkfill)" />
        <ellipse
          cx="48"
          cy="50"
          rx="22"
          ry="20"
          fill="none"
          stroke="rgba(58,46,30,0.10)"
          strokeWidth="0.4"
          strokeDasharray="0.6 1.4"
        />

        <g transform="translate(92,10)" opacity="0.55">
          <circle r="3" fill="none" stroke="rgba(58,46,30,0.25)" strokeWidth="0.2" />
          <path d="M 0 -3 L 0.5 0 L 0 3 L -0.5 0 Z" fill="#b86b3a" />
          <text y="-3.6" fontSize="1.6" textAnchor="middle" fill="rgba(58,46,30,0.55)" fontFamily="JetBrains Mono, monospace">
            N
          </text>
        </g>

        {allPts.length > 1 && (
          <>
            <path
              d={smoothPath(allPts)}
              fill="none"
              stroke="rgba(184,107,58,0.18)"
              strokeWidth="2.2"
              strokeLinecap="round"
              strokeLinejoin="round"
              style={{
                strokeDasharray: 600,
                strokeDashoffset: 600,
                animation: 'route-draw 1.6s cubic-bezier(.55,.1,.25,1) .15s forwards',
              }}
            />
            <path
              d={smoothPath(allPts)}
              fill="none"
              stroke="url(#routegrad)"
              strokeWidth="0.8"
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeDasharray="2.2 1.6"
              style={{
                strokeDashoffset: 600,
                animation: 'route-draw 1.6s cubic-bezier(.55,.1,.25,1) .15s forwards',
              }}
            />
          </>
        )}

        {areas.map((a) => {
          const onRoute = allAreasOnRoute.includes(a.id);
          const isToday = a.id === todayArea;
          return (
            <g key={a.id}>
              <circle
                cx={a.x}
                cy={a.y}
                r={isToday ? 1.6 : onRoute ? 1.0 : 0.6}
                fill={isToday ? '#b86b3a' : onRoute ? '#5b5345' : 'rgba(58,46,30,0.30)'}
                stroke={isToday ? '#fbf6eb' : 'transparent'}
                strokeWidth="0.4"
              />
              <text
                x={a.x + 2.2}
                y={a.y + 0.6}
                fontSize="2.1"
                fill={isToday ? '#2c2820' : onRoute ? 'rgba(58,46,30,0.78)' : 'rgba(58,46,30,0.42)'}
                fontFamily="JetBrains Mono, monospace"
                fontWeight={isToday ? 600 : 400}
                style={{
                  animation: 'label-fade .5s ease both',
                  animationDelay: `${0.35 + Math.random() * 0.4}s`,
                  opacity: 0,
                }}
              >
                {a.name}
              </text>
            </g>
          );
        })}

        {allPts.map((p, i) => {
          const delay = 0.25 + i * 0.22;
          const isActive = i === activeDay;
          return (
            <g
              key={'d' + i}
              style={{
                transformOrigin: `${p.x}px ${p.y - 4}px`,
                animation: 'pin-pop .55s cubic-bezier(.34,1.56,.64,1) both',
                animationDelay: `${delay}s`,
              }}
            >
              {isActive && (
                <circle
                  cx={p.x}
                  cy={p.y - 4}
                  r="3.6"
                  fill="url(#glow)"
                  style={{
                    transformOrigin: `${p.x}px ${p.y - 4}px`,
                    animation: 'pin-pulse 1.8s ease-in-out infinite',
                    animationDelay: `${delay + 0.4}s`,
                  }}
                />
              )}
              <path
                d={`M ${p.x} ${p.y - 1} Q ${p.x - 2.6} ${p.y - 4} ${p.x} ${p.y - 7.2} Q ${p.x + 2.6} ${p.y - 4} ${p.x} ${p.y - 1} Z`}
                fill={isActive ? '#b86b3a' : '#fbf6eb'}
                stroke={isActive ? '#a35d2f' : '#b86b3a'}
                strokeWidth="0.35"
              />
              <circle cx={p.x} cy={p.y - 4.2} r="1.4" fill={isActive ? '#fbf6eb' : '#b86b3a'} />
              <text
                x={p.x}
                y={p.y - 3.6}
                fontSize="1.8"
                fill={isActive ? '#b86b3a' : '#fbf6eb'}
                textAnchor="middle"
                fontFamily="JetBrains Mono, monospace"
                fontWeight="700"
              >
                {i + 1}
              </text>
            </g>
          );
        })}
      </svg>

      <div className="map-overlay">
        <div className="tag neon">
          <div className="tag-dot" />
          {dest?.label || destinationKey}
        </div>
        <div className="tag">
          Day {activeDay + 1} · {todayPt?.name || ''}
        </div>
      </div>
      <div className="map-legend">
        <div className="lg-row"><div className="sw" style={{ background: '#b86b3a' }} />Today</div>
        <div className="lg-row"><div className="sw" style={{ background: '#5b5345' }} />On route</div>
        <div className="lg-row"><div className="sw" style={{ background: 'rgba(58,46,30,0.30)' }} />Other areas</div>
      </div>
    </div>
  );
}
