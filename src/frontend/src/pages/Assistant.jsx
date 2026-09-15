import { useState } from 'react';
import { agentQuery } from '../api/client';

const SUGGESTIONS = [
  'Which shipments are affected by the Rotterdam port strike?',
  'What are rerouting options for shipments blocked at Suez Canal?',
  'Are there idle fleet assets near the disrupted region?',
  'Show me all critical cold chain excursions.',
];

function TypingIndicator() {
  return (
    <div className="typing-indicator">
      <span /><span /><span />
    </div>
  );
}

export default function Assistant() {
  const [query,   setQuery]   = useState('');
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);

  const submit = (q) => {
    const text = q || query;
    if (!text.trim()) return;
    setLoading(true);
    setHistory(h => [...h, { role: 'user', text }]);
    agentQuery(text)
      .then(r => {
        setHistory(h => [...h, {
          role: 'assistant',
          text: r.data.response,
          meta: `Tools: ${r.data.tools_used.join(', ')} · ${r.data.summary.affected_shipments} affected · ${r.data.summary.idle_fleet_assets} idle assets · ${r.data.summary.cold_chain_alerts} cold chain alerts`,
        }]);
        setLoading(false);
        setQuery('');
      })
      .catch(() => {
        setHistory(h => [...h, { role: 'assistant', text: 'Error contacting the assistant. Is the backend running?' }]);
        setLoading(false);
      });
  };

  return (
    <div style={{ maxWidth: 760 }}>
      <h2 className="page-title">Supply Chain Assistant</h2>
      <p style={{ color: 'var(--color-text-muted)', fontSize: 14, marginBottom: 'var(--space-5)', lineHeight: 1.6 }}>
        Ask questions in natural language. The assistant chains all 4 analysis tools and responds with actionable insights.
      </p>

      {/* Suggestion chips */}
      <div className="suggestion-chips">
        {SUGGESTIONS.map(s => (
          <button key={s} className="suggestion-chip" onClick={() => submit(s)}>
            {s}
          </button>
        ))}
      </div>

      {/* Chat history */}
      <div className="chat-history">
        {history.map((m, i) => (
          <div
            key={i}
            className={`chat-bubble chat-bubble--${m.role}`}
          >
            <div className="chat-bubble__role">
              {m.role === 'user' ? 'You' : 'Assistant'}
            </div>
            <div>{m.text}</div>
            {m.meta && <div className="chat-meta">{m.meta}</div>}
          </div>
        ))}
        {loading && <TypingIndicator />}
      </div>

      {/* Input bar */}
      <div className="chat-input-bar">
        <input
          className="chat-input"
          value={query}
          onChange={e => setQuery(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && submit()}
          placeholder="Ask a question about your supply chain…"
        />
        <button
          className="btn btn--primary"
          onClick={() => submit()}
          disabled={loading || !query.trim()}
        >
          Ask
        </button>
      </div>
    </div>
  );
}
