import { useEffect, useState } from 'react';
import { getImpact, reroute } from '../api/client';

const severityClass = (s) => s >= 8 ? 'badge badge--red' : s >= 5 ? 'badge badge--orange' : 'badge badge--green';
const priorityClass = (p) => p === 'high' ? 'badge badge--red' : 'badge badge--grey';

function SkeletonTable() {
  return (
    <table className="data-table">
      <thead>
        <tr>
          {['Ref', 'Origin → Dest', 'Cargo', 'Carrier', 'Priority', 'Disruption', 'Severity', 'Action'].map(h => (
            <th key={h}>{h}</th>
          ))}
        </tr>
      </thead>
      <tbody>
        {[0, 1, 2].map(i => (
          <tr key={i} className="skeleton-row">
            {[0, 1, 2, 3, 4, 5, 6, 7].map(j => (
              <td key={j}><div className="skeleton skeleton-cell" /></td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
}

export default function Disruptions() {
  const [shipments,      setShipments]      = useState([]);
  const [loading,        setLoading]        = useState(true);
  const [rerouteData,    setRerouteData]    = useState({});
  const [loadingReroute, setLoadingReroute] = useState({});

  useEffect(() => {
    getImpact()
      .then(r => { setShipments(r.data.shipments); setLoading(false); })
      .catch(()  => setLoading(false));
  }, []);

  const handleReroute = (id) => {
    setLoadingReroute(p => ({ ...p, [id]: true }));
    reroute(id)
      .then(r => {
        setRerouteData(p => ({ ...p, [id]: r.data }));
        setLoadingReroute(p => ({ ...p, [id]: false }));
      })
      .catch(() => setLoadingReroute(p => ({ ...p, [id]: false })));
  };

  if (loading) return <SkeletonTable />;

  if (!shipments.length) return (
    <p className="empty-state empty-state--ok">No shipments currently affected by active disruptions.</p>
  );

  return (
    <div>
      <h2 className="page-title">
        Affected Shipments
        <span className="page-title__count">({shipments.length})</span>
      </h2>

      <table className="data-table">
        <thead>
          <tr>
            {['Ref', 'Origin → Dest', 'Cargo', 'Carrier', 'Priority', 'Disruption', 'Severity', 'Action'].map(h => (
              <th key={h}>{h}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {shipments.map(s => (
            <>
              <tr key={s.shipment_id}>
                <td style={{ fontWeight: 700 }}>{s.shipment_ref}</td>
                <td>{s.origin} → {s.destination}</td>
                <td>{s.cargo_type}</td>
                <td>{s.carrier}</td>
                <td><span className={priorityClass(s.priority)}>{s.priority}</span></td>
                <td style={{ fontSize: 12 }}>
                  {s.disruption.event_type.replace('_', ' ')} — {s.disruption.region}
                </td>
                <td>
                  <span className={severityClass(s.impact_severity)}>
                    {s.impact_severity}/10
                  </span>
                </td>
                <td>
                  <button
                    className="btn btn--primary btn--sm"
                    onClick={() => handleReroute(s.shipment_id)}
                    disabled={!!loadingReroute[s.shipment_id]}
                  >
                    {loadingReroute[s.shipment_id] ? '…' : 'Reroute'}
                  </button>
                </td>
              </tr>

              {rerouteData[s.shipment_id] && (
                <tr key={`r-${s.shipment_id}`} className="row-expanded">
                  <td colSpan={8}>
                    <div className="reroute-panel">
                      <div className="reroute-panel__title">
                        Rerouting Options — {s.shipment_ref}
                      </div>
                      {rerouteData[s.shipment_id].recommendations.map(rec => (
                        <div key={rec.rank} className="reroute-option">
                          <div className="reroute-option__rank">{rec.rank}</div>
                          <div>{rec.details}</div>
                        </div>
                      ))}
                    </div>
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
