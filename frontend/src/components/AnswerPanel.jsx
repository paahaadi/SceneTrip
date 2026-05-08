import { useEffect, useRef, useState } from 'react';

// One-question-at-a-time answer panel — switches input shape based on
// question kind. Mirrors the prototype's AnswerPanel.
export function AnswerPanel({ q, onSubmit, onSkip }) {
  const [val, setVal] = useState(q.kind === 'chip-multi' ? [] : '');
  const inputRef = useRef(null);

  useEffect(() => {
    setVal(q.kind === 'chip-multi' ? [] : '');
    if (q.kind === 'text' && inputRef.current) inputRef.current.focus();
  }, [q.id, q.kind]);

  if (q.kind === 'text') {
    return (
      <div className="answer-panel">
        <form
          className="answer-input"
          onSubmit={(e) => {
            e.preventDefault();
            if (val.trim()) onSubmit(val.trim());
          }}
        >
          <input
            ref={inputRef}
            type={q.inputType || 'text'}
            placeholder={q.placeholder}
            value={val}
            onChange={(e) => setVal(e.target.value)}
            aria-label={q.q}
          />
          <button className="btn primary" type="submit">Send →</button>
        </form>
        <div className="answer-skip">
          <button type="button" onClick={() => onSkip(q.default)}>
            Use suggested · {String(q.default)}
          </button>
        </div>
      </div>
    );
  }

  if (q.kind === 'chip') {
    return (
      <div className="answer-panel">
        <div className="answer-grid" role="radiogroup" aria-label={q.q}>
          {q.options.map((o) => (
            <button key={o} className="chip" onClick={() => onSubmit(o)} role="radio" aria-checked={false}>
              {o}
            </button>
          ))}
        </div>
        <div className="answer-skip">
          <button type="button" onClick={() => onSkip(q.default)}>
            Use suggested · {q.default}
          </button>
        </div>
      </div>
    );
  }

  if (q.kind === 'chip-rich') {
    return (
      <div className="answer-panel">
        <div className="answer-grid" style={{ flexDirection: 'column', alignItems: 'stretch' }}>
          {q.options.map((o) => (
            <button
              key={o.v}
              className="chip"
              style={{
                textAlign: 'left',
                borderRadius: 12,
                padding: '12px 14px',
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'flex-start',
                gap: 2,
              }}
              onClick={() => onSubmit({ value: o.v, label: o.label })}
            >
              <span style={{ fontWeight: 600, fontSize: 14 }}>{o.label}</span>
              <span
                style={{
                  fontSize: 12,
                  color: 'var(--ink-3)',
                  fontFamily: 'var(--mono)',
                  letterSpacing: '0.04em',
                }}
              >
                {o.sub}
              </span>
            </button>
          ))}
        </div>
        <div className="answer-skip">
          <button
            type="button"
            onClick={() => {
              const def = q.options.find((o) => o.v === q.default);
              onSkip({ value: def.v, label: def.label });
            }}
          >
            Use suggested · {q.options.find((o) => o.v === q.default).label}
          </button>
        </div>
      </div>
    );
  }

  if (q.kind === 'chip-multi') {
    const toggle = (o) => setVal((v) => (v.includes(o) ? v.filter((x) => x !== o) : [...v, o]));
    return (
      <div className="answer-panel">
        <div className="answer-grid" role="group" aria-label={q.q}>
          {q.options.map((o) => (
            <button
              key={o}
              className="chip"
              data-on={val.includes(o) ? 1 : 0}
              onClick={() => toggle(o)}
              aria-pressed={val.includes(o)}
            >
              {o}
            </button>
          ))}
        </div>
        <div
          style={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            marginTop: 10,
            gap: 10,
            flexWrap: 'wrap',
          }}
        >
          <div className="answer-skip" style={{ margin: 0 }}>
            <button type="button" onClick={() => onSkip(q.default)}>
              Use suggested · {q.default.join(', ')}
            </button>
          </div>
          <button className="btn primary" disabled={!val.length} onClick={() => onSubmit(val)}>
            Continue →
          </button>
        </div>
      </div>
    );
  }

  return null;
}
