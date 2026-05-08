import { useEffect, useRef, useState } from 'react';
import { Bubble, TypingBubble } from './Bubble.jsx';
import { AnswerPanel } from './AnswerPanel.jsx';
import { PERSONAS, DESTINATIONS } from '../data/personas.js';

const wait = (ms) => new Promise((r) => setTimeout(r, ms));
const interp = (s, ctx) => (s || '').replace(/\{(\w+)\}/g, (_, k) => ctx[k] ?? '');

// Conversational state machine. One question at a time, typing indicator
// before each bot turn, light "ack" lines after key answers (name, persona,
// destination) for warmth.
export function ChatWindow({ script, profile, onDone }) {
  const [msgs, setMsgs] = useState([]);
  const [qIdx, setQIdx] = useState(0);
  const [typing, setTyping] = useState(false);
  const [answers, setAnswers] = useState({});
  const threadRef = useRef(null);

  // initial intro notes + first question
  useEffect(() => {
    let cancelled = false;
    (async () => {
      let i = 0;
      while (script[i] && script[i].kind === 'note') {
        if (cancelled) return;
        setTyping(true);
        await wait(700);
        if (cancelled) return;
        setTyping(false);
        setMsgs((m) => [...m, { kind: 'bot', text: script[i].text }]);
        await wait(280);
        i++;
      }
      if (script[i]) {
        setTyping(true);
        await wait(750);
        if (cancelled) return;
        setTyping(false);
        setMsgs((m) => [...m, { kind: 'bot', text: interp(script[i].q, profile) }]);
        setQIdx(i);
      }
    })();
    return () => {
      cancelled = true;
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    if (threadRef.current) {
      threadRef.current.scrollTop = threadRef.current.scrollHeight + 600;
    }
  }, [msgs.length, typing]);

  const submit = async (raw) => {
    const q = script[qIdx];
    if (!q) return;
    const labelFor = (v) => {
      if (typeof v === 'object' && v && 'label' in v) return v.label;
      if (Array.isArray(v)) return v.join(', ');
      return String(v);
    };
    const stored =
      typeof raw === 'object' && raw && 'value' in raw ? raw.value : raw;
    const nextAnswers = { ...answers, [q.id]: stored };
    setAnswers(nextAnswers);
    setMsgs((m) => [...m, { kind: 'user', text: labelFor(raw) }]);
    setQIdx(-1);
    await wait(380);

    let next = qIdx + 1;
    while (script[next] && script[next].kind === 'note') {
      setTyping(true);
      await wait(550);
      setTyping(false);
      setMsgs((m) => [...m, { kind: 'bot', text: script[next].text }]);
      next++;
    }

    if (!script[next]) {
      setTyping(true);
      await wait(700);
      setTyping(false);
      onDone(nextAnswers);
      return;
    }

    setTyping(true);
    await wait(720 + Math.random() * 350);
    setTyping(false);

    // small acknowledgements that color the chat — don't change semantics
    if (q.id === 'name') {
      setMsgs((m) => [...m, { kind: 'bot', text: `Nice to meet you, ${stored}.` }]);
      await wait(280); setTyping(true); await wait(500); setTyping(false);
    } else if (q.id === 'persona') {
      const p = PERSONAS[stored];
      if (p) {
        setMsgs((m) => [...m, { kind: 'bot', text: `${p.tag} energy — got it.` }]);
        await wait(280); setTyping(true); await wait(500); setTyping(false);
      }
    } else if (q.id === 'destination') {
      const dest = DESTINATIONS[stored];
      setMsgs((m) => [
        ...m,
        { kind: 'bot', text: `${dest?.label || stored}. Excellent. A few last details and I'll plan.` },
      ]);
      await wait(280); setTyping(true); await wait(500); setTyping(false);
    }

    const nq = script[next];
    setMsgs((m) => [...m, { kind: 'bot', text: interp(nq.q, { ...profile, ...nextAnswers }) }]);
    setQIdx(next);
  };

  const q = qIdx >= 0 ? script[qIdx] : null;

  return (
    <div className="chat">
      <div className="chat-thread" ref={threadRef}>
        {msgs.map((m, i) => (
          <Bubble key={i} kind={m.kind} header={m.header}>
            {m.text}
          </Bubble>
        ))}
        {typing && <TypingBubble />}
      </div>
      {q && <AnswerPanel q={q} onSubmit={submit} onSkip={submit} />}
    </div>
  );
}
