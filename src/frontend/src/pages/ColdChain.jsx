import { useEffect, useState } from 'react';
import { getColdChain } from '../api/client';
import StatCard from '../components/StatCard';

const SEV_BADGE = {
  'CRITICAL':         'badge badge--critical',
  'REPORTABLE BREACH':'badge badge--reportable',
  'MINOR DEVIATION':  'badge badge--minor',
};

function SkeletonTable() {
  return (
    <table className="data-table">
      <thead>
        <tr>
          {['Shipment', 'Cargo Type', 'Safe Range', 'Recorded Temp', 'Deviation', 'Severity', 'Recommended Action'].map(h => (
            <th key={h}>{h}</th>
          ))}
        </tr>
      </thead>
      <tbody>
        {[0, 1, 2].map(i => (
          <tr key={i} className="skeleton-row">
            {[0, 1, 2, 3, 4, 5, 6].map(j => (
              <td key={j}><div className="skeleton skeleton-cell" /></td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
}

export default function ColdChain() {
  const [data,    setData]    = useState(null);
  const [loading, setLoading] = useState(true);
  const [error,   setError]   = useState(null);

  useEffect(() => {
    getColdChain()
      .then(r => { setData(r.data); setLoading(false); })
      .catch((err) => {
        console.error('ColdChain fetch failed:', err);
        setError('Failed to load cold chain data. Is the backend running?');
        setLoading(false);
      });
  }, []);

  if (loading) return (
    <>
      <div style={{ display: 'flex', gap: 'var(--space-4)', flexWrap: 'wrap', marginBottom: 'var(--space-6)' }}>
        <div className="skeleton skeleton-card" />
        <div className="skeleton skeleton-card" />
        <div className="skeleton skeleton-card" />
      </div>
      <SkeletonTable />
    </>
  );

  if (error) return <p className="empty-state empty-state--error">{error}</p>;

  if (!data || !data.alerts.length) return (
    <p className="empty-state empty-state--ok">No cold chain excursions detected.</p>
  );

  return (
    <div>
      <div style={{ display: 'flex', gap: 'var(--space-4)', flexWrap: 'wrap', marginBottom: 'var(--space-6)' }}>
        <StatCard icon="🔴" value={data.critical}   label="Critical"   colorClass="red"    />
        <StatCard icon="🟠" value={data.reportable} label="Reportable" colorClass="orange" />
        <StatCard icon="🟡" value={data.minor}       label="Minor"      colorClass="yellow" />
      </div>

      <h2 className="page-title">
        Excursion Alerts
        <span className="page-title__count">({data.total_alerts})</span>
      </h2>

      <table className="data-table">
        <thead>
          <tr>
            {['Shipment', 'Cargo Type', 'Safe Range', 'Recorded Temp', 'Deviation', 'Severity', 'Recommended Action'].map(h => (
              <th key={h}>{h}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.alerts.map((a, i) => (
            <tr key={i} className={a.severity === 'CRITICAL' ? 'row--critical' : ''}>
              <td style={{ fontWeight: 700 }}>{a.shipment_ref}</td>
              <td>{a.cargo_type}</td>
              <td>{a.safe_range}</td>
              <td style={{ fontWeight: 700, color: 'var(--color-red)' }}>{a.excursion_temp}°C</td>
              <td>+{Math.abs(a.deviation)}°C</td>
              <td>
                <span className={SEV_BADGE[a.severity] || 'badge badge--grey'}>
                  {a.severity || 'UNKNOWN'}
                </span>
              </td>
              <td style={{ fontSize: 12, color: 'var(--color-text-muted)', maxWidth: 280 }}>
                {a.action}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
