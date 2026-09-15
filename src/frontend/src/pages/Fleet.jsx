import { useEffect, useState } from 'react';
import { getFleetIdle } from '../api/client';

const typeColor = { truck: '#2980b9', reefer: '#8e44ad', vessel: '#16a085', container: '#d35400' };
const badge = (text) => (
  <span style={{ background: typeColor[text] || '#7f8c8d', color: '#fff', borderRadius: 4, padding: '2px 8px', fontSize: 12 }}>
    {text}
  </span>
);

export default function Fleet() {
  const [assets, setAssets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [region, setRegion] = useState('');

  const load = (r) => {
    setLoading(true);
    getFleetIdle(r || undefined).then(res => { setAssets(res.data.assets); setLoading(false); }).catch(() => setLoading(false));
  };

  useEffect(() => { load(); }, []);

  const regions = ['', 'Rotterdam', 'South China Sea', 'Suez Canal', 'Los Angeles'];

  return (
    <div>
      <div style={{ display: 'flex', alignItems: 'center', gap: 16, marginBottom: 20 }}>
        <h2 style={{ margin: 0 }}>Idle Fleet Assets <span style={{ fontSize: 16, color: '#888' }}>({assets.length})</span></h2>
        <select
          value={region}
          onChange={e => { setRegion(e.target.value); load(e.target.value); }}
          style={{ padding: '6px 10px', fontSize: 14, borderRadius: 4, border: '1px solid #ccc' }}
        >
          {regions.map(r => <option key={r} value={r}>{r || 'All Regions'}</option>)}
        </select>
      </div>
      {loading ? <p>Loading fleet data...</p> : !assets.length ? <p style={{ color: '#27ae60' }}>No idle assets in this region.</p> : (
        <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: 14 }}>
          <thead>
            <tr style={{ background: '#f0f0f0' }}>
              {['Ref', 'Type', 'Location', 'Region', 'Capacity (t)', 'Near Disruption', 'Suggested For'].map(h => (
                <th key={h} style={{ padding: '8px 12px', textAlign: 'left', borderBottom: '2px solid #ddd' }}>{h}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {assets.map(a => (
              <tr key={a.asset_id} style={{ borderBottom: '1px solid #eee' }}>
                <td style={{ padding: '8px 12px', fontWeight: 600 }}>{a.asset_ref}</td>
                <td style={{ padding: '8px 12px' }}>{badge(a.asset_type)}</td>
                <td style={{ padding: '8px 12px' }}>{a.location}</td>
                <td style={{ padding: '8px 12px' }}>{a.region}</td>
                <td style={{ padding: '8px 12px' }}>{a.capacity_tonnes}</td>
                <td style={{ padding: '8px 12px' }}>
                  {a.near_disruption ? <span style={{ color: '#c0392b', fontWeight: 600 }}>⚠ Yes</span> : <span style={{ color: '#27ae60' }}>No</span>}
                </td>
                <td style={{ padding: '8px 12px', fontSize: 12, color: '#555' }}>{a.suggested_for || '—'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
