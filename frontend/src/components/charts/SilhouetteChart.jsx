import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ReferenceLine } from 'recharts'
import { silhouetteData } from '../../data/mockData'

const Tip = ({ active, payload }) => {
  if (!active || !payload?.length) return null
  return (
    <div className="custom-tooltip">
      <div className="label">K = {payload[0].payload.k}</div>
      <div className="val">Score: {payload[0].value.toFixed(3)}</div>
    </div>
  )
}

export default function SilhouetteChart() {
  return (
    <ResponsiveContainer width="100%" height={260}>
      <LineChart data={silhouetteData} margin={{ top: 30, right: 20, left: 10, bottom: 10 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
        <XAxis dataKey="k" tick={{ fill: '#94a3b8', fontSize: 11 }} axisLine={false} tickLine={false}
          label={{ value: 'Số cụm K', position: 'insideBottom', offset: -5, fill: '#475569', fontSize: 11 }} />
        <YAxis domain={[0.28, 0.46]} tick={{ fill: '#94a3b8', fontSize: 10 }} axisLine={false} tickLine={false} />
        <Tooltip content={<Tip />} />
        <ReferenceLine x={5} stroke="#22c55e" strokeDasharray="5 3"
          label={{ value: 'K=5 cao nhất', position: 'top', fill: '#22c55e', fontSize: 11 }} />
        <Line type="monotone" dataKey="score" stroke="#22c55e" strokeWidth={2.5}
          dot={{ fill: '#22c55e', r: 4, strokeWidth: 0 }}
          activeDot={{ r: 6, fill: '#22c55e', stroke: 'rgba(34,197,94,0.3)', strokeWidth: 4 }} />
      </LineChart>
    </ResponsiveContainer>
  )
}
