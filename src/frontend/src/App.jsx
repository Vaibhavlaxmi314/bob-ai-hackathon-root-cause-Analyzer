import { useState } from 'react';
import Dashboard from './pages/Dashboard';
import Disruptions from './pages/Disruptions';
import Fleet from './pages/Fleet';
import ColdChain from './pages/ColdChain';
import Assistant from './pages/Assistant';

const TABS = [
  { id: 'dashboard',   label: '📊 Overview' },
  { id: 'disruptions', label: '🚨 Disruptions' },
  { id: 'fleet',       label: '🚛 Fleet Assets' },
  { id: 'coldchain',   label: '🌡 Cold Chain' },
  { id: 'assistant',   label: '🤖 Assistant' },
];

const PAGES = {
  dashboard:   <Dashboard />,
  disruptions: <Disruptions />,
  fleet:       <Fleet />,
  coldchain:   <ColdChain />,
  assistant:   <Assistant />,
};

const ChainIcon = () => (
  <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
    <path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/>
    <path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/>
  </svg>
);

export default function App() {
  const [tab, setTab] = useState('dashboard');

  return (
    <>
      <header className="app-header">
        <div className="app-header__logo" aria-hidden="true">
          <ChainIcon />
        </div>
        <div className="app-header__titles">
          <h1 className="app-header__title">Supply Chain Disruption Assistant</h1>
          <p className="app-header__subtitle">Fleet Utilisation Optimizer &nbsp;·&nbsp; Powered by IBM Bob &amp; watsonx.ai</p>
        </div>
      </header>

      <nav className="tab-bar" role="navigation" aria-label="Main navigation">
        {TABS.map(t => (
          <button
            key={t.id}
            onClick={() => setTab(t.id)}
            className={`tab-bar__item${tab === t.id ? ' tab-bar__item--active' : ''}`}
            aria-current={tab === t.id ? 'page' : undefined}
          >
            {t.label}
          </button>
        ))}
      </nav>

      <main className="page-content">
        {PAGES[tab]}
      </main>
    </>
  );
}
