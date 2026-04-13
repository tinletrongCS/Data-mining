import { Radar, RadarChart, PolarGrid, PolarAngleAxis, ResponsiveContainer, Legend, Tooltip } from 'recharts'
import { rfmRadarData } from '../../data/mockData'

const axes = [
  { key: 'recency',   label: 'Độ mới (Recency)' },
  { key: 'frequency', label: 'Tần suất (Frequency)' },
  { key: 'monetary',  label: 'Giá trị (Monetary)' },
]

// Reshape for Recharts RadarChart
const radarFormatted = axes.map(a => {
  const obj = { axis: a.label }
  rfmRadarData.forEach(d => { obj[d.cluster] = d[a.key] })
  return obj
})

const COLORS = { 'At Risk': '#ef4444', 'Regular': '#22c55e', 'Loyal': '#eab308', 'VIP': '#3b82f6' }

const Tip = ({ active, payload }) => {
  if (!active || !payload?.length) return null
  return (
    <div className="custom-tooltip">
      <div className="label">{payload[0]?.payload?.axis}</div>
      {payload.map(p => (
        <div key={p.name} style={{ color: COLORS[p.name], fontSize: 12, marginTop: 3 }}>
          {p.name}: {(p.value * 100).toFixed(0)}%
        </div>
      ))}
    </div>
  )
}

export default function RFMRadarChart() {
  return (
    <ResponsiveContainer width="100%" height={300}>
      <RadarChart data={radarFormatted} margin={{ top: 10, right: 30, bottom: 10, left: 30 }}>
        <PolarGrid stroke="rgba(255,255,255,0.1)" />
        <PolarAngleAxis dataKey="axis" tick={{ fill: '#94a3b8', fontSize: 11 }} />
        {rfmRadarData.map(d => (
          <Radar key={d.cluster} name={d.cluster} dataKey={d.cluster}
            stroke={COLORS[d.cluster]} fill={COLORS[d.cluster]} fillOpacity={0.15} strokeWidth={2} />
        ))}
        <Legend iconType="circle" wrapperStyle={{ fontSize: 12, color: '#94a3b8', paddingTop: 8 }} />
        <Tooltip content={<Tip />} />
      </RadarChart>
    </ResponsiveContainer>
  )
}
