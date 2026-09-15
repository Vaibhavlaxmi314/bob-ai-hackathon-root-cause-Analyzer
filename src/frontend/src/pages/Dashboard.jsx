import { useEffect, useState } from 'react';
import { getImpact, getFleetIdle, getColdChain } from '../api/client';

const card = (label, value, color) => (
  <div style={{ background: color, borderRadius: 8, padding: '20px 28px', minWidth: 160, color: '#fff' }}>
    <div style={{ fontSize: 32, fontWeight: 700 }}>{value}</div>
    <div style={{ fontSize: 13, marginTop: 4, opacity: 0.9 }}>{label}</div>
  </div>
);

export default function Dashboard() {
  const [data, setData] = useState({ affected: 0, idle: 0, critical: 0, alerts: 0 });

  useEffect(() => {
    Promise.all([getImpact(), getFleetIdle(), getColdChain()]).then(([imp, fleet, cold]) => {
      setData({
        affected: imp.data.total_affected,
        idle: fleet.data.total_idle,
        alerts: cold.data.total_alerts,
        critical: cold.data.critical,
      });
    }).catch(() => {});
  }, []);

  return (
    <div>
      <h2 style={{ marginBottom: 24 }}>Operations Overview</h2>
      <div style={{ display: 'flex', gap: 16, flexWrap: 'wrap' }}>
        {card('Affected Shipments', data.affected, '#c0392b')}
        {card('Idle Fleet Assets', data.idle, '#2980b9')}
        {card('Cold Chain Alerts', data.alerts, '#8e44ad')}
        {card('Critical Excursions', data.critical, '#e67e22')}
      </div>
      <p style={{ marginTop: 32, color: '#555', fontSize: 14 }}>
        Use the tabs above to drill into Disruptions, Fleet Assets, or Cold Chain alerts.
        Use the Assistant tab to ask questions in natural language.
      </p>
    </div>
  );
}
