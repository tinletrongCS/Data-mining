import { correlationData } from '../../data/mockData'

const getColor = (v) => {
  if (v >= 0) {
    const t = v
    const r = Math.round(239 * t), g = Math.round(68 * t), b = Math.round(68 * t)
    return `rgba(${r},${g},${b},${0.15 + 0.75 * t})`
  } else {
    const t = -v
    const r = Math.round(59 * t), g = Math.round(130 * t), b = Math.round(246 * t)
    return `rgba(${r},${g},${b},${0.15 + 0.75 * t})`
  }
}

export default function CorrelationHeatmap() {
  const { labels, matrix } = correlationData
  const n = labels.length

  return (
    <div style={{ overflowX: 'auto' }}>
      <table style={{ borderCollapse: 'separate', borderSpacing: 4, margin: '0 auto' }}>
        <thead>
          <tr>
            <th style={{ width: 80 }} />
            {labels.map(l => (
              <th key={l} style={{ color: '#94a3b8', fontSize: 11, fontWeight: 500, padding: '0 4px 8px', textAlign: 'center', width: 72 }}>
                {l}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {matrix.map((row, i) => (
            <tr key={i}>
              <td style={{ color: '#94a3b8', fontSize: 11, fontWeight: 500, paddingRight: 8, textAlign: 'right' }}>
                {labels[i]}
              </td>
              {row.map((v, j) => (
                <td key={j} style={{
                  background: i === j ? 'rgba(255,255,255,0.08)' : getColor(v),
                  borderRadius: 6,
                  width: 72, height: 52,
                  textAlign: 'center',
                  verticalAlign: 'middle',
                  fontSize: 12,
                  fontWeight: 600,
                  color: i === j ? '#94a3b8' : '#e2e8f0',
                }}>
                  {v.toFixed(2)}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
      <div style={{ display: 'flex', justifyContent: 'center', gap: 24, marginTop: 14, fontSize: 11, color: '#94a3b8' }}>
        <span style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
          <span style={{ width: 32, height: 10, background: 'rgba(59,130,246,0.7)', borderRadius: 3, display: 'inline-block' }} />
          Tương quan âm
        </span>
        <span style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
          <span style={{ width: 32, height: 10, background: 'rgba(239,68,68,0.7)', borderRadius: 3, display: 'inline-block' }} />
          Tương quan dương
        </span>
      </div>
    </div>
  )
}
