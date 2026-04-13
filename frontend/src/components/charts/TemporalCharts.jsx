import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts'
import { hourlyOrders, weekdayOrders } from '../../data/mockData'

const HourTip = ({ active, payload }) => {
  if (!active || !payload?.length) return null
  return (
    <div className="custom-tooltip">
      <div className="label">Giờ {payload[0].payload.h}:00</div>
      <div className="val">{payload[0].value.toLocaleString()} đơn</div>
    </div>
  )
}

const DayTip = ({ active, payload }) => {
  if (!active || !payload?.length) return null
  return (
    <div className="custom-tooltip">
      <div className="label">{payload[0].payload.day}</div>
      <div className="val">{payload[0].value.toLocaleString()} đơn</div>
    </div>
  )
}

const DAY_COLORS = ['#6366f1','#6366f1','#6366f1','#6366f1','#00d4ff','#22c55e','#22c55e']

export function HourlyChart() {
  return (
    <ResponsiveContainer width="100%" height={220}>
      <LineChart data={hourlyOrders} margin={{ top: 5, right: 10, left: 0, bottom: 5 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
        <XAxis dataKey="h" tick={{ fill: '#94a3b8', fontSize: 10 }} axisLine={false} tickLine={false}
          tickFormatter={v => `${v}h`} interval={3} />
        <YAxis tick={{ fill: '#94a3b8', fontSize: 10 }} axisLine={false} tickLine={false}
          tickFormatter={v => v >= 1000 ? `${(v/1000).toFixed(0)}K` : v} />
        <Tooltip content={<HourTip />} cursor={{ stroke: 'rgba(255,255,255,0.1)' }} />
        <Line type="monotone" dataKey="v" stroke="#00d4ff" strokeWidth={2.5}
          dot={false} activeDot={{ r: 4, fill: '#00d4ff' }} />
      </LineChart>
    </ResponsiveContainer>
  )
}

export function WeekdayChart() {
  return (
    <ResponsiveContainer width="100%" height={220}>
      <BarChart data={weekdayOrders} margin={{ top: 5, right: 10, left: 0, bottom: 5 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" vertical={false} />
        <XAxis dataKey="day" tick={{ fill: '#94a3b8', fontSize: 11 }} axisLine={false} tickLine={false} />
        <YAxis tick={{ fill: '#94a3b8', fontSize: 10 }} axisLine={false} tickLine={false}
          tickFormatter={v => `${(v/1000).toFixed(0)}K`} />
        <Tooltip content={<DayTip />} cursor={{ fill: 'rgba(255,255,255,0.04)' }} />
        <Bar dataKey="orders" radius={[4, 4, 0, 0]}>
          {weekdayOrders.map((_, i) => <Cell key={i} fill={DAY_COLORS[i]} />)}
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  )
}
