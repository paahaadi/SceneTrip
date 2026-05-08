import { useEffect, useState } from 'react';

const STEPS = [
  'Loading persona rules…',
  'Querying Google Places · candidate set',
  'Estimating Google Routes feasibility',
  'Generating itinerary with Gemini',
  'Validating against persona constraints',
  'Done.',
];

// Animated progress while the backend works. We tick through the steps
// independent of network — once the API resolves we surface that via
// `actuallyDone`. If the network finishes before we tick to the end, we
// jump to the last step.
export function Planning({ actuallyDone, onComplete }) {
  const [i, setI] = useState(0);

  useEffect(() => {
    let alive = true;
    (async () => {
      for (let k = 0; k < STEPS.length - 1; k++) {
        if (!alive) return;
        setI(k);
        await new Promise((r) => setTimeout(r, 600 + Math.random() * 220));
        if (actuallyDone) break;
      }
      if (alive && actuallyDone) {
        setI(STEPS.length - 1);
        await new Promise((r) => setTimeout(r, 280));
        onComplete?.();
      }
    })();
    return () => { alive = false; };
  // we deliberately ignore `actuallyDone` updates after the loop starts —
  // the loop checks the latest value via closure-recreate on next render.
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [actuallyDone]);

  return (
    <div className="planning">
      <div className="ring" />
      <h2>Planning your scene…</h2>
      <div className="steps">
        {STEPS.map((s, k) => (
          <div key={k} className="row" data-active={k === i ? 1 : 0} data-done={k < i ? 1 : 0}>
            <div className="marker" />
            <div>{s}</div>
          </div>
        ))}
      </div>
    </div>
  );
}
