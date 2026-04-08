export default function ChartCard({ title, subtitle, badge, children, className = '' }) {
  return (
    <div className={`chart-card ${className}`}>
      <div className="chart-header">
        <div>
          <div className="chart-title">{title}</div>
          {subtitle && <div className="chart-subtitle">{subtitle}</div>}
        </div>
        {badge && <span className="chart-badge">{badge}</span>}
      </div>
      {children}
    </div>
  )
}
