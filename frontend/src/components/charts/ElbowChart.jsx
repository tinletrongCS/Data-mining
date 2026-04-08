import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ReferenceLine } from 'recharts'
import { elbowData } from '../../data/mockData'

const Tip = ({ active, payload }) => {
  if (!active || !payload?.length) return null
  return (
    <div className="custom-tooltip">
      <div className="label">K = {payload[0].payload.k}</div>
      <div className="val">WCSS: {payload[0].value.toLocaleString()}</div>
    </div>
  )
}

export default function ElbowChart() {
  return (
    <ResponsiveContainer width="100%" height={260}>
      <LineChart data={elbowData} margin={{ top: 10, right: 20, left: 10, bottom: 10 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
        <XAxis dataKey="k" tick={{ fill: '#94a3b8', fontSize: 11 }} axisLine={false} tickLine={false}
          label={{ value: 'Số cụm K', position: 'insideBottom', offset: -5, fill: '#475569', fontSize: 11 }} />
        <YAxis tick={{ fill: '#94a3b8', fontSize: 10 }} axisLine={false} tickLine={false}
          tickFormatter={v => `${(v/1000).toFixed(0)}K`} />
        <Tooltip content={<Tip />} />
        <ReferenceLine x={4} stroke="#eab308" strokeDasharray="5 3"
          label={{ value: 'K=4 tối ưu', position: 'top', fill: '#eab308', fontSize: 11 }} />
        <Line type="monotone" dataKey="wcss" stroke="#00d4ff" strokeWidth={2.5}
          dot={{ fill: '#00d4ff', r: 4, strokeWidth: 0 }}
          activeDot={{ r: 6, fill: '#00d4ff', stroke: 'rgba(0,212,255,0.3)', strokeWidth: 4 }} />
      </LineChart>
    </ResponsiveContainer>
  )
}
