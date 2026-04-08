import { ScatterChart, Scatter, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'
import { clusterScatter, clusterProfiles } from '../../data/mockData'

const COLORS = { 0: '#ef4444', 1: '#22c55e', 2: '#eab308', 3: '#3b82f6' }

const Tip = ({ active, payload }) => {
  if (!active || !payload?.length) return null
  const d = payload[0].payload
  return (
    <div className="custom-tooltip">
      <div className="label" style={{ color: COLORS[d.cluster] }}>
        {clusterProfiles[d.cluster]?.nameVi}
      </div>
      <div style={{ fontSize: 12, color: '#94a3b8', marginTop: 4 }}>Recency: <span style={{ color: '#e2e8f0' }}>{d.recency} ngày</span></div>
      <div style={{ fontSize: 12, color: '#94a3b8' }}>Đơn hàng: <span style={{ color: '#e2e8f0' }}>{d.total_orders}</span></div>
      <div style={{ fontSize: 12, color: '#94a3b8' }}>AOV: <span style={{ color: '#e2e8f0' }}>${d.avg_order_value}</span></div>
    </div>
  )
}

// Group by cluster
const byCluster = [0,1,2,3].map(c => clusterScatter.filter(p => p.cluster === c))

export default function ClusterScatterChart() {
  return (
    <>
      <ResponsiveContainer width="100%" height={300}>
        <ScatterChart margin={{ top: 10, right: 20, left: 0, bottom: 10 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
          <XAxis dataKey="x" type="number" name="Log(Recency)"
            tick={{ fill: '#94a3b8', fontSize: 10 }} axisLine={false} tickLine={false}
            label={{ value: 'Log(Recency)', position: 'insideBottom', offset: -5, fill: '#475569', fontSize: 11 }} />
          <YAxis dataKey="y" type="number" name="Log(Total Orders)"
            tick={{ fill: '#94a3b8', fontSize: 10 }} axisLine={false} tickLine={false}
            label={{ value: 'Log(Orders)', angle: -90, position: 'insideLeft', fill: '#475569', fontSize: 11 }} />
          <Tooltip content={<Tip />} />
          {byCluster.map((pts, ci) => (
            <Scatter key={ci} data={pts} fill={COLORS[ci]} opacity={0.75} />
          ))}
        </ScatterChart>
      </ResponsiveContainer>

      <div className="legend">
        {clusterProfiles.map(p => (
          <div key={p.id} className="legend-item">
            <div className="legend-dot" style={{ background: p.color }} />
            Cụm {p.id}: {p.nameVi}
          </div>
        ))}
      </div>
    </>
  )
}
