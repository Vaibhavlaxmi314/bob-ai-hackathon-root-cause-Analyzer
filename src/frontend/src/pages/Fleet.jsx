import { useEffect, useState } from 'react';
import { getFleetIdle } from '../api/client';

const TYPE_BADGE = {
  truck:     'badge badge--blue',
  reefer:    'badge badge--purple',
  vessel:    'badge badge--green',
  container: 'badge badge--orange',
};

function SkeletonTable() {
  return (
    <table className="data-table">
      <thead>
        <tr>
          {['Ref', 'Type', 'Location', 'Region', 'Capacity (t)', 'Near Disruption', 'Suggested For'].map(h => (
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

export default function Fleet() {
  const [assets,  setAssets]  = useState([]);
  const [loading, setLoading] = useState(true);
  const [error,   setError]   = useState(null);
  const [region,  setRegion]  = useState('');

  const load = (r) => {
    setLoading(true);
    setError(null);
    getFleetIdle(r || undefined)
      .then(res => { setAssets(res.data.assets); setLoading(false); })
      .catch((err) => {
        console.error('Fleet fetch failed:', err);
        setError('Failed to load fleet data. Is the backend running?');
        setLoading(false);
      });
  };

  useEffect(() => { load(); }, []);

  const regions = ['', 'Rotterdam', 'South China Sea', 'Suez Canal', 'Los Angeles'];

  return (
    <div>
      <div className="filter-bar">
        <h2 className="page-title" style={{ margin: 0 }}>
          Idle Fleet Assets
          <span className="page-title__count">({assets.length})</span>
        </h2>
        <select
          className="select"
          value={region}
          onChange={e => { setRegion(e.target.value); load(e.target.value); }}
        >
          {regions.map(r => (
            <option key={r} value={r}>{r || 'All Regions'}</option>
          ))}
        </select>
      </div>

      {loading ? (
        <SkeletonTable />
      ) : error ? (
        <p className="empty-state empty-state--error">{error}</p>
      ) : !assets.length ? (
        <p className="empty-state empty-state--ok">No idle assets in this region.</p>
      ) : (
        <table className="data-table">
          <thead>
            <tr>
              {['Ref', 'Type', 'Location', 'Region', 'Capacity (t)', 'Near Disruption', 'Suggested For'].map(h => (
                <th key={h}>{h}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {assets.map(a => (
              <tr key={a.asset_id}>
                <td style={{ fontWeight: 700 }}>{a.asset_ref}</td>
                <td>
                  <span className={TYPE_BADGE[a.asset_type] || 'badge badge--grey'}>
                    {a.asset_type}
                  </span>
                </td>
                <td>{a.location}</td>
                <td>{a.region}</td>
                <td>{a.capacity_tonnes}</td>
                <td>
                  {a.near_disruption
                    ? <span className="badge badge--red">⚠ Yes</span>
                    : <span className="badge badge--green">No</span>
                  }
                </td>
                <td style={{ fontSize: 12, color: 'var(--color-text-muted)' }}>
                  {a.suggested_for || '—'}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
