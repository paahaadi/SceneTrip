export function Bubble({ kind, header, children }) {
  return (
    <div className={`bubble ${kind}`}>
      {header && <div className="mini-h">{header}</div>}
      {children}
    </div>
  );
}

export function TypingBubble() {
  return (
    <div className="bubble bot">
      <div className="typing">
        <span /><span /><span />
      </div>
    </div>
  );
}
