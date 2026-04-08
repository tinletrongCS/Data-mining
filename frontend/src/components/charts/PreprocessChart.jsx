import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'
import { preprocessComparison } from '../../data/mockData'

const Tip = ({ active, payload, label }) => {
  if (!active || !payload?.length) return null
  return (
    <div className="custom-tooltip">
      <div className="label">{label}</div>
      <div className="val">{payload[0].value.toLocaleString()} sản phẩm</div>
    </div>
  )
}

export default function PreprocessChart() {
  return (
    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 20 }}>
      <div>
        <div style={{ fontSize: 12, color: '#ef4444', fontWeight: 600, marginBottom: 10 }}>
          ❌ Trước xử lý — Dữ liệu bị lệch (Skewed)
        </div>
        <ResponsiveContainer width="100%" height={220}>
          <BarChart data={preprocessComparison.before} margin={{ top: 5, right: 10, left: 0, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" vertical={false} />
            <XAxis dataKey="bin" tick={{ fill: '#94a3b8', fontSize: 10 }} axisLine={false} tickLine={false} />
            <YAxis tick={{ fill: '#94a3b8', fontSize: 10 }} axisLine={false} tickLine={false}
              tickFormatter={v => v >= 1000 ? `${(v/1000).toFixed(0)}K` : v} />
            <Tooltip content={<Tip />} cursor={{ fill: 'rgba(255,255,255,0.04)' }} />
            <Bar dataKey="c" fill="#6b7280" radius={[3, 3, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>

      <div>
        <div style={{ fontSize: 12, color: '#22c55e', fontWeight: 600, marginBottom: 10 }}>
          ✅ Sau xử lý — Phân phối chuẩn hơn
        </div>
        <ResponsiveContainer width="100%" height={220}>
          <BarChart data={preprocessComparison.after} margin={{ top: 5, right: 10, left: 0, bottom: 5 }}>
            <defs>
              <linearGradient id="afterGrad" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor="#00d4ff" stopOpacity={0.9} />
                <stop offset="100%" stopColor="#00d4ff" stopOpacity={0.3} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" vertical={false} />
            <XAxis dataKey="bin" tick={{ fill: '#94a3b8', fontSize: 10 }} axisLine={false} tickLine={false} />
            <YAxis tick={{ fill: '#94a3b8', fontSize: 10 }} axisLine={false} tickLine={false}
              tickFormatter={v => v >= 1000 ? `${(v/1000).toFixed(0)}K` : v} />
            <Tooltip content={<Tip />} cursor={{ fill: 'rgba(255,255,255,0.04)' }} />
            <Bar dataKey="c" fill="url(#afterGrad)" radius={[3, 3, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}
