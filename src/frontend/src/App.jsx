import { useState } from 'react';
import Dashboard from './pages/Dashboard';
import Disruptions from './pages/Disruptions';
import Fleet from './pages/Fleet';
import ColdChain from './pages/ColdChain';
import Assistant from './pages/Assistant';

const TABS = [
  { id: 'dashboard',    label: '📊 Overview' },
  { id: 'disruptions',  label: '🚨 Disruptions' },
  { id: 'fleet',        label: '🚛 Fleet Assets' },
  { id: 'coldchain',    label: '🌡 Cold Chain' },
  { id: 'assistant',    label: '🤖 Assistant' },
];

const PAGES = {
  dashboard:   <Dashboard />,
  disruptions: <Disruptions />,
  fleet:       <Fleet />,
  coldchain:   <ColdChain />,
  assistant:   <Assistant />,
};

export default function App() {
  const [tab, setTab] = useState('dashboard');

  return (
    <div style={{ fontFamily: '-apple-system, "Segoe UI", sans-serif', minHeight: '100vh', background: '#f8f9fa' }}>
      {/* Header */}
      <div style={{ background: '#1a1a2e', color: '#fff', padding: '16px 32px' }}>
        <h1 style={{ margin: 0, fontSize: 20, fontWeight: 700 }}>
          Supply Chain Disruption Assistant
        </h1>
        <p style={{ margin: '4px 0 0', fontSize: 13, opacity: 0.7 }}>
          Fleet Utilisation Optimizer · Powered by IBM Bob + watsonx.ai
        </p>
      </div>

      {/* Tab bar */}
      <div style={{ background: '#fff', borderBottom: '2px solid #e0e0e0', display: 'flex', paddingLeft: 32 }}>
        {TABS.map(t => (
          <button key={t.id} onClick={() => setTab(t.id)} style={{
            padding: '12px 20px', border: 'none', background: 'none', cursor: 'pointer',
            fontSize: 14, fontWeight: tab === t.id ? 700 : 400,
            borderBottom: tab === t.id ? '3px solid #2980b9' : '3px solid transparent',
            color: tab === t.id ? '#2980b9' : '#444',
            marginBottom: -2,
          }}>{t.label}</button>
        ))}
      </div>

      {/* Page content */}
      <div style={{ padding: '32px', maxWidth: 1200, margin: '0 auto' }}>
        {PAGES[tab]}
      </div>
    </div>
  );
}
