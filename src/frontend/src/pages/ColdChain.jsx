import { useEffect, useState } from 'react';
import { getColdChain } from '../api/client';

const severityColor = { 'CRITICAL': '#c0392b', 'REPORTABLE BREACH': '#e67e22', 'MINOR DEVIATION': '#f1c40f' };
const severityTextColor = { 'CRITICAL': '#fff', 'REPORTABLE BREACH': '#fff', 'MINOR DEVIATION': '#333' };

const badge = (sev) => (
  <span style={{
    background: severityColor[sev] || '#95a5a6',
    color: severityTextColor[sev] || '#fff',
    borderRadius: 4, padding: '2px 8px', fontSize: 12, fontWeight: 700
  }}>{sev || 'UNKNOWN'}</span>
);

export default function ColdChain() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getColdChain().then(r => { setData(r.data); setLoading(false); }).catch(() => setLoading(false));
  }, []);

  if (loading) return <p>Scanning IoT sensor logs...</p>;
  if (!data || !data.alerts.length) return <p style={{ color: '#27ae60' }}>No cold chain excursions detected.</p>;

  return (
    <div>
      <div style={{ display: 'flex', gap: 16, marginBottom: 24, flexWrap: 'wrap' }}>
        <div style={{ background: '#c0392b', color: '#fff', borderRadius: 8, padding: '12px 20px' }}>
          <strong style={{ fontSize: 24 }}>{data.critical}</strong> <span style={{ fontSize: 13 }}>Critical</span>
        </div>
        <div style={{ background: '#e67e22', color: '#fff', borderRadius: 8, padding: '12px 20px' }}>
          <strong style={{ fontSize: 24 }}>{data.reportable}</strong> <span style={{ fontSize: 13 }}>Reportable</span>
        </div>
        <div style={{ background: '#f1c40f', color: '#333', borderRadius: 8, padding: '12px 20px' }}>
          <strong style={{ fontSize: 24 }}>{data.minor}</strong> <span style={{ fontSize: 13 }}>Minor</span>
        </div>
      </div>
      <h2>Excursion Alerts <span style={{ fontSize: 16, color: '#888' }}>({data.total_alerts})</span></h2>
      <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: 14 }}>
        <thead>
          <tr style={{ background: '#f0f0f0' }}>
            {['Shipment', 'Cargo Type', 'Safe Range', 'Recorded Temp', 'Deviation', 'Severity', 'Recommended Action'].map(h => (
              <th key={h} style={{ padding: '8px 12px', textAlign: 'left', borderBottom: '2px solid #ddd' }}>{h}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.alerts.map((a, i) => (
            <tr key={i} style={{ borderBottom: '1px solid #eee', background: a.severity === 'CRITICAL' ? '#fdf0f0' : undefined }}>
              <td style={{ padding: '8px 12px', fontWeight: 600 }}>{a.shipment_ref}</td>
              <td style={{ padding: '8px 12px' }}>{a.cargo_type}</td>
              <td style={{ padding: '8px 12px' }}>{a.safe_range}</td>
              <td style={{ padding: '8px 12px', fontWeight: 700, color: '#c0392b' }}>{a.excursion_temp}°C</td>
              <td style={{ padding: '8px 12px' }}>+{Math.abs(a.deviation)}°C</td>
              <td style={{ padding: '8px 12px' }}>{badge(a.severity)}</td>
              <td style={{ padding: '8px 12px', fontSize: 12, color: '#444', maxWidth: 300 }}>{a.action}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
