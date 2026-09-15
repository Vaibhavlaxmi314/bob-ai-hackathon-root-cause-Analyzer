import { useState } from 'react';
import { agentQuery } from '../api/client';

export default function Assistant() {
  const [query, setQuery] = useState('');
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);

  const suggestions = [
    'Which shipments are affected by the Rotterdam port strike?',
    'What are rerouting options for shipments blocked at Suez Canal?',
    'Are there idle fleet assets near the disrupted region?',
    'Show me all critical cold chain excursions.',
  ];

  const submit = (q) => {
    const text = q || query;
    if (!text.trim()) return;
    setLoading(true);
    setHistory(h => [...h, { role: 'user', text }]);
    agentQuery(text).then(r => {
      setHistory(h => [...h, {
        role: 'assistant',
        text: r.data.response,
        meta: `Tools used: ${r.data.tools_used.join(', ')} | Affected: ${r.data.summary.affected_shipments} shipments, ${r.data.summary.idle_fleet_assets} idle assets, ${r.data.summary.cold_chain_alerts} cold chain alerts`
      }]);
      setLoading(false);
      setQuery('');
    }).catch(() => {
      setHistory(h => [...h, { role: 'assistant', text: 'Error contacting the assistant. Is the backend running?' }]);
      setLoading(false);
    });
  };

  return (
    <div style={{ maxWidth: 760 }}>
      <h2>Supply Chain Assistant</h2>
      <p style={{ color: '#555', fontSize: 14, marginBottom: 16 }}>
        Ask questions in natural language. The assistant chains all 4 analysis tools and responds with actionable insights.
      </p>

      {/* Suggestion chips */}
      <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8, marginBottom: 20 }}>
        {suggestions.map(s => (
          <button key={s} onClick={() => submit(s)} style={{
            padding: '6px 12px', fontSize: 13, borderRadius: 16,
            border: '1px solid #2980b9', color: '#2980b9', background: '#fff', cursor: 'pointer'
          }}>{s}</button>
        ))}
      </div>

      {/* Chat history */}
      <div style={{ minHeight: 200, marginBottom: 16 }}>
        {history.map((m, i) => (
          <div key={i} style={{
            marginBottom: 12, padding: '12px 16px', borderRadius: 8,
            background: m.role === 'user' ? '#eaf4fb' : '#f4f4f4',
            borderLeft: `4px solid ${m.role === 'user' ? '#2980b9' : '#8e44ad'}`
          }}>
            <div style={{ fontWeight: 600, fontSize: 12, color: '#888', marginBottom: 4 }}>
              {m.role === 'user' ? 'YOU' : 'ASSISTANT'}
            </div>
            <div style={{ fontSize: 14, lineHeight: 1.6 }}>{m.text}</div>
            {m.meta && <div style={{ fontSize: 11, color: '#aaa', marginTop: 8 }}>{m.meta}</div>}
          </div>
        ))}
        {loading && <div style={{ color: '#888', fontSize: 14 }}>Analysing...</div>}
      </div>

      {/* Input */}
      <div style={{ display: 'flex', gap: 8 }}>
        <input
          value={query}
          onChange={e => setQuery(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && submit()}
          placeholder="Ask a question about your supply chain..."
          style={{ flex: 1, padding: '10px 14px', fontSize: 14, borderRadius: 6, border: '1px solid #ccc' }}
        />
        <button onClick={() => submit()} disabled={loading || !query.trim()} style={{
          padding: '10px 20px', background: '#2980b9', color: '#fff',
          border: 'none', borderRadius: 6, cursor: 'pointer', fontSize: 14
        }}>Ask</button>
      </div>
    </div>
  );
}
