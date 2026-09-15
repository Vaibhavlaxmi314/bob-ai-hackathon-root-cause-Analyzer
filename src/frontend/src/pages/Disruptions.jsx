import { useEffect, useState } from 'react';
import { getImpact, reroute } from '../api/client';

const severityColor = (s) => s >= 8 ? '#c0392b' : s >= 5 ? '#e67e22' : '#27ae60';
const badge = (text, color) => (
  <span style={{ background: color, color: '#fff', borderRadius: 4, padding: '2px 8px', fontSize: 12, fontWeight: 600 }}>
    {text}
  </span>
);

export default function Disruptions() {
  const [shipments, setShipments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [rerouteData, setRerouteData] = useState({});
  const [loadingReroute, setLoadingReroute] = useState({});

  useEffect(() => {
    getImpact().then(r => { setShipments(r.data.shipments); setLoading(false); }).catch(() => setLoading(false));
  }, []);

  const handleReroute = (id) => {
    setLoadingReroute(p => ({ ...p, [id]: true }));
    reroute(id).then(r => {
      setRerouteData(p => ({ ...p, [id]: r.data }));
      setLoadingReroute(p => ({ ...p, [id]: false }));
    }).catch(() => setLoadingReroute(p => ({ ...p, [id]: false })));
  };

  if (loading) return <p>Loading disruption impact...</p>;
  if (!shipments.length) return <p style={{ color: '#27ae60' }}>No shipments currently affected.</p>;

  return (
    <div>
      <h2>Affected Shipments <span style={{ fontSize: 16, color: '#888' }}>({shipments.length})</span></h2>
      <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: 14 }}>
        <thead>
          <tr style={{ background: '#f0f0f0' }}>
            {['Ref', 'Origin → Dest', 'Cargo', 'Carrier', 'Priority', 'Disruption', 'Severity', 'Action'].map(h => (
              <th key={h} style={{ padding: '8px 12px', textAlign: 'left', borderBottom: '2px solid #ddd' }}>{h}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {shipments.map(s => (
            <>
              <tr key={s.shipment_id} style={{ borderBottom: '1px solid #eee' }}>
                <td style={{ padding: '8px 12px', fontWeight: 600 }}>{s.shipment_ref}</td>
                <td style={{ padding: '8px 12px' }}>{s.origin} → {s.destination}</td>
                <td style={{ padding: '8px 12px' }}>{s.cargo_type}</td>
                <td style={{ padding: '8px 12px' }}>{s.carrier}</td>
                <td style={{ padding: '8px 12px' }}>{badge(s.priority, s.priority === 'high' ? '#c0392b' : '#7f8c8d')}</td>
                <td style={{ padding: '8px 12px', fontSize: 12 }}>{s.disruption.event_type.replace('_', ' ')} — {s.disruption.region}</td>
                <td style={{ padding: '8px 12px' }}>
                  <span style={{ color: severityColor(s.impact_severity), fontWeight: 700 }}>{s.impact_severity}/10</span>
                </td>
                <td style={{ padding: '8px 12px' }}>
                  <button
                    onClick={() => handleReroute(s.shipment_id)}
                    disabled={!!loadingReroute[s.shipment_id]}
                    style={{ padding: '4px 12px', cursor: 'pointer', background: '#2980b9', color: '#fff', border: 'none', borderRadius: 4, fontSize: 12 }}
                  >
                    {loadingReroute[s.shipment_id] ? '...' : 'Reroute'}
                  </button>
                </td>
              </tr>
              {rerouteData[s.shipment_id] && (
                <tr key={`r-${s.shipment_id}`} style={{ background: '#eaf4fb' }}>
                  <td colSpan={8} style={{ padding: '10px 16px', fontSize: 13 }}>
                    <strong>Rerouting Options for {s.shipment_ref}:</strong>
                    {rerouteData[s.shipment_id].recommendations.map(rec => (
                      <div key={rec.rank} style={{ marginTop: 6 }}>
                        <strong>Option {rec.rank}:</strong> {rec.details}
                      </div>
                    ))}
                  </td>
                </tr>
              )}
            </>
          ))}
        </tbody>
      </table>
    </div>
  );
}
