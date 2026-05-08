import { useState } from 'react';
import { PERSONAS, DESTINATIONS, REPLAN_CHIPS } from '../data/personas.js';
import { MapPane } from './MapPane.jsx';

// One day = one expandable card, with the persona-fit narrative pinned
// underneath. Replan chips + free-text input persist below the day list.
export function ItineraryCard({
  destination,
  persona,
  profile,
  days,
  showWhy = true,
  showMap = true,
  replanState,
  onReplan,
  thinking,
}) {
  const dest = DESTINATIONS[destination] || { label: destination, sub: '' };
  const personaMeta = PERSONAS[persona];
  const [activeDay, setActiveDay] = useState(0);
  const [openDays, setOpenDays] = useState({ 0: true, 1: true, 2: true, 3: true, 4: true });
  const [replanText, setReplanText] = useState('');

  const submit = (text) => {
    if (!text.trim() || thinking) return;
    onReplan(text);
    setReplanText('');
  };

  return (
    <div className={`it-shell ${showMap ? 'with-map' : ''}`}>
      <div style={{ display: 'flex', flexDirection: 'column', minHeight: 0 }}>
        <div className="it-list">
          <div className="it-head">
            <div
              className="row"
              style={{ alignItems: 'center', justifyContent: 'space-between' }}
            >
              <div>
                <h1>
                  {dest.label.split(',')[0]}
                  <em>.</em>
                </h1>
                <div className="meta" style={{ marginTop: 6 }}>
                  <span><b>{dest.sub}</b></span>
                  <span>·</span>
                  <span>{personaMeta?.name}</span>
                  <span>·</span>
                  <span>{profile.budget || 'Mid-range'}</span>
                </div>
              </div>
              <div className="tag neon">
                <div className="tag-dot" />Live plan
              </div>
            </div>
            {replanState?.summary && (
              <div className="bubble bot" style={{ maxWidth: '100%', marginTop: 6 }}>
                <div className="mini-h">// last replan</div>
                {replanState.summary}
              </div>
            )}
          </div>

          {days.map((d, i) => {
            const open = openDays[i] !== false;
            const isChanged = replanState?.changed?.includes(i);
            return (
              <div key={i} className={`day-card ${isChanged ? 'is-changed' : ''}`}>
                <div
                  className="day-h"
                  onClick={() => {
                    setOpenDays((o) => ({ ...o, [i]: !open }));
                    setActiveDay(i);
                  }}
                >
                  <div className="num"><em>{String(i + 1).padStart(2, '0')}</em></div>
                  <div className="title">
                    <div className="t">{d.title}</div>
                    <div className="s">{d.sub}</div>
                  </div>
                  <div className="change-badge"><div className="tag-dot" />Updated</div>
                  <div className="kbd">{open ? '▾' : '▸'}</div>
                </div>
                {open && (
                  <div className="day-body">
                    {d.slots.map((s, j) => (
                      <div className="slot" key={j}>
                        <div className="when">{s.when}</div>
                        <div className="stops">
                          {s.stops.map((st, k) => (
                            <div
                              className="stop"
                              key={k}
                              data-kind={st.kind || ''}
                              data-changed={st._added ? 'add' : st._removed ? 'rem' : ''}
                            >
                              <div className="dot" />
                              <div className="body">
                                <div className="n">{st.name}</div>
                                {st.meta && <div className="meta">{st.meta}</div>}
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>
                    ))}
                    {showWhy && d.why && (
                      <div className="why">
                        <div className="ic">i</div>
                        <div>
                          <b style={{ color: 'var(--ink)', fontWeight: 500 }}>Why this fits you · </b>
                          {d.why}
                        </div>
                      </div>
                    )}
                  </div>
                )}
              </div>
            );
          })}
          <div style={{ height: 8 }} />
        </div>

        <div className="replan">
          <div className="replan-chips">
            {REPLAN_CHIPS.map((c) => (
              <button key={c} className="chip" onClick={() => submit(c)} disabled={thinking}>
                {c}
              </button>
            ))}
          </div>
          <form
            className="replan-input"
            onSubmit={(e) => {
              e.preventDefault();
              submit(replanText);
            }}
          >
            <input
              placeholder={thinking ? 'Replanning…' : 'Tell SceneTrip what to change…'}
              value={replanText}
              onChange={(e) => setReplanText(e.target.value)}
              disabled={thinking}
              aria-label="Replan instruction"
            />
            <button type="submit" disabled={thinking || !replanText.trim()}>
              {thinking ? '…' : 'Replan'}
            </button>
          </form>
        </div>
      </div>

      {showMap && <MapPane destinationKey={destination} days={days} activeDay={activeDay} />}
    </div>
  );
}
