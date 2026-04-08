import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ReferenceLine } from 'recharts'
import { salesTrend } from '../../data/mockData'

const Tip = ({ active, payload, label }) => {
  if (!active || !payload?.length) return null
  return (
    <div className="custom-tooltip">
      <div className="label">{label}</div>
      <div className="val">{payload[0].value.toLocaleString()} đơn hàng</div>
    </div>
  )
}

// Sample every 3rd point for performance
const sampled = salesTrend.filter((_, i) => i % 3 === 0)

export default function SalesTrendLine() {
  return (
    <ResponsiveContainer width="100%" height={280}>
      <AreaChart data={sampled} margin={{ top: 5, right: 10, left: 0, bottom: 5 }}>
        <defs>
          <linearGradient id="trendGrad" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor="#00d4ff" stopOpacity={0.3} />
            <stop offset="100%" stopColor="#00d4ff" stopOpacity={0.01} />
          </linearGradient>
        </defs>
        <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
        <XAxis dataKey="label" tick={{ fill: '#94a3b8', fontSize: 10 }} axisLine={false} tickLine={false}
          interval={9} />
        <YAxis tick={{ fill: '#94a3b8', fontSize: 10 }} axisLine={false} tickLine={false}
          tickFormatter={v => `${(v/1000).toFixed(0)}K`} />
        <Tooltip content={<Tip />} />
        <ReferenceLine x="29 thg 11" stroke="#eab308" strokeDasharray="4 4" label={{ value: 'Black Friday', fill: '#eab308', fontSize: 10 }} />
        <Area type="monotone" dataKey="orders" stroke="#00d4ff" strokeWidth={2}
          fill="url(#trendGrad)" dot={false} activeDot={{ r: 4, fill: '#00d4ff' }} />
      </AreaChart>
    </ResponsiveContainer>
  )
}
