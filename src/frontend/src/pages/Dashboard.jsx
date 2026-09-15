import { useEffect, useState } from 'react';
import { getImpact, getFleetIdle, getColdChain } from '../api/client';
import StatCard from '../components/StatCard';

function SkeletonCard() {
  return <div className="skeleton skeleton-card" />;
}

export default function Dashboard() {
  const [data, setData]       = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError]     = useState(null);

  useEffect(() => {
    Promise.all([getImpact(), getFleetIdle(), getColdChain()])
      .then(([imp, fleet, cold]) => {
        setData({
          affected: imp.data.total_affected,
          idle:     fleet.data.total_idle,
          alerts:   cold.data.total_alerts,
          critical: cold.data.critical,
        });
        setLoading(false);
      })
      .catch((err) => {
        console.error('Dashboard fetch failed:', err);
        setError('Failed to load dashboard data. Is the backend running?');
        setLoading(false);
      });
  }, []);

  if (error) return <p className="empty-state empty-state--error">{error}</p>;

  return (
    <div>
      <h2 className="page-title">Operations Overview</h2>

      <div style={{ display: 'flex', gap: 'var(--space-4)', flexWrap: 'wrap', marginBottom: 'var(--space-7)' }}>
        {loading ? (
          <>
            <SkeletonCard />
            <SkeletonCard />
            <SkeletonCard />
            <SkeletonCard />
          </>
        ) : (
          <>
            <StatCard icon="🚨" value={data.affected} label="Affected Shipments"  colorClass="red"    />
            <StatCard icon="🚛" value={data.idle}     label="Idle Fleet Assets"   colorClass="blue"   />
            <StatCard icon="🌡" value={data.alerts}   label="Cold Chain Alerts"   colorClass="purple" />
            <StatCard icon="⚠️" value={data.critical} label="Critical Excursions" colorClass="orange" />
          </>
        )}
      </div>

      <p style={{ color: 'var(--color-text-muted)', fontSize: 14, lineHeight: 1.6 }}>
        Use the tabs above to drill into Disruptions, Fleet Assets, or Cold Chain alerts.
        Use the <strong>Assistant</strong> tab to ask questions in natural language.
      </p>
    </div>
  );
}
