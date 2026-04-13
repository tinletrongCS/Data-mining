import { timeHeatmapData } from '../../data/mockData'

const DAYS = ['Thứ 2','Thứ 3','Thứ 4','Thứ 5','Thứ 6','Thứ 7','CN']
const MAX_VAL = 142

const toColor = (v) => {
  const t = Math.min(v / MAX_VAL, 1)
  if (t < 0.33) {
    const s = t / 0.33
    return `rgba(99,102,241,${0.1 + 0.4 * s})`
  } else if (t < 0.66) {
    const s = (t - 0.33) / 0.33
    return `rgba(0,${Math.round(180 + 32 * s)},${Math.round(255 - 100 * s)},${0.5 + 0.2 * s})`
  } else {
    const s = (t - 0.66) / 0.34
    return `rgba(${Math.round(0 + 234 * s)},${Math.round(212 - 145 * s)},${Math.round(255 - 237 * s)},${0.7 + 0.3 * s})`
  }
}

export default function TimeHeatmap() {
  const hours = Array.from({ length: 24 }, (_, i) => i)

  return (
    <div style={{ overflowX: 'auto' }}>
      <div style={{ display: 'grid', gridTemplateColumns: '52px repeat(24, 1fr)', gap: 2, minWidth: 680 }}>
        {/* Header */}
        <div />
        {hours.map(h => (
          <div key={h} style={{ textAlign: 'center', fontSize: 9, color: '#475569', padding: '0 0 4px' }}>
            {h % 4 === 0 ? `${h}h` : ''}
          </div>
        ))}

        {/* Rows */}
        {DAYS.map((day, di) => (
          <>
            <div key={`lbl-${di}`} style={{ fontSize: 11, color: '#94a3b8', display: 'flex', alignItems: 'center', justifyContent: 'flex-end', paddingRight: 8 }}>
              {day}
            </div>
            {timeHeatmapData[di]?.values.map((cell) => (
              <div
                key={`${di}-${cell.hour}`}
                title={`${day} ${cell.hour}h: ${cell.value}`}
                style={{
                  background: toColor(cell.value),
                  borderRadius: 3,
                  height: 28,
                  transition: 'transform 0.15s',
                  cursor: 'default',
                }}
                onMouseEnter={e => e.currentTarget.style.transform = 'scale(1.3)'}
                onMouseLeave={e => e.currentTarget.style.transform = 'scale(1)'}
              />
            ))}
          </>
        ))}
      </div>

      {/* Color scale */}
      <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginTop: 14, fontSize: 11, color: '#94a3b8' }}>
        <span>Ít</span>
        <div style={{ flex: 1, height: 8, borderRadius: 4, background: 'linear-gradient(to right, rgba(99,102,241,0.2), rgba(0,212,255,0.6), rgba(234,179,8,0.9))', maxWidth: 200 }} />
        <span>Nhiều</span>
      </div>
    </div>
  )
}
