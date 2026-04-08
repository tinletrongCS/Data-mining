import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend, Cell } from 'recharts'
import { clusterMeans, clusterProfiles } from '../../data/mockData'

const CLUSTER_COLORS = ['#ef4444', '#22c55e', '#eab308', '#3b82f6']

const buildData = (key) =>
  clusterProfiles.map((p, i) => ({
    name: `Cụm ${i}`,
    value: clusterMeans[key][i],
    color: CLUSTER_COLORS[i],
  }))

const Tip = ({ active, payload, unit }) => {
  if (!active || !payload?.length) return null
  return (
    <div className="custom-tooltip">
      <div className="label">{payload[0].payload.name}</div>
      <div className="val">{payload[0].value.toLocaleString()}{unit}</div>
    </div>
  )
}

const MiniTip = (unit) => (props) => <Tip {...props} unit={unit} />

function ClusterBar({ data, unit, height = 180 }) {
  return (
    <ResponsiveContainer width="100%" height={height}>
      <BarChart data={data} margin={{ top: 5, right: 10, left: 0, bottom: 5 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" vertical={false} />
        <XAxis dataKey="name" tick={{ fill: '#94a3b8', fontSize: 10 }} axisLine={false} tickLine={false} />
        <YAxis tick={{ fill: '#94a3b8', fontSize: 10 }} axisLine={false} tickLine={false} />
        <Tooltip content={MiniTip(unit)} cursor={{ fill: 'rgba(255,255,255,0.04)' }} />
        <Bar dataKey="value" radius={[4, 4, 0, 0]}>
          {data.map((d, i) => <Cell key={i} fill={d.color} />)}
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  )
}

export default function ClusterBarComparison() {
  const metrics = [
    { key: 'recency',         label: 'Recency (ngày)',       unit: ' ngày' },
    { key: 'total_orders',    label: 'Số đơn trung bình',    unit: ' đơn'  },
    { key: 'total_spend',     label: 'Tổng chi tiêu ($)',    unit: '$'     },
    { key: 'avg_order_value', label: 'Giá trị TB đơn ($)',   unit: '$'     },
  ]

  return (
    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 20 }}>
      {metrics.map(m => (
        <div key={m.key}>
          <div style={{ fontSize: 12, color: '#94a3b8', marginBottom: 8, fontWeight: 500 }}>{m.label}</div>
          <ClusterBar data={buildData(m.key)} unit={m.unit} />
        </div>
      ))}
    </div>
  )
}
