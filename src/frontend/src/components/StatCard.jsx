export default function StatCard({ icon, value, label, colorClass }) {
  return (
    <div className={`stat-card stat-card--${colorClass}`}>
      <div className="stat-card__icon">{icon}</div>
      <div className="stat-card__value">{value}</div>
      <div className="stat-card__label">{label}</div>
    </div>
  );
}
