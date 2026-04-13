import { correlationData } from '../../data/mockData'

const getColor = (v) => {
  // Đảm bảo v là số (phòng trường hợp dữ liệu mock bị lưu dưới dạng string)
  const val = Number(v);
  
  // Nếu = 0: Độc lập (Không tương quan) -> Trả về màu xám trung tính
  if (val === 0) {
    return 'rgba(255, 255, 255, 0.05)'; 
  }

  const t = Math.abs(val);
  // Đặt độ trong suốt (alpha) thấp nhất là 0.15 để ô luôn có màu nền nhẹ
  const alpha = 0.15 + 0.85 * t;

  if (val > 0) {
    // Tương quan dương: Màu Đỏ (Red)
    return `rgba(239, 68, 68, ${alpha})`;
  } else {
    // Tương quan âm: Màu Xanh dương (Blue)
    return `rgba(59, 130, 246, ${alpha})`;
  }
}

export default function CorrelationHeatmap() {
  const { labels, matrix } = correlationData

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
              {row.map((v, j) => {
                const val = Number(v);
                return (
                  <td key={j} style={{
                    background: i === j ? 'rgba(255,255,255,0.08)' : getColor(v),
                    borderRadius: 6,
                    width: 72, height: 52,
                    textAlign: 'center',
                    verticalAlign: 'middle',
                    fontSize: 12,
                    fontWeight: 600,
                    // Nếu là đường chéo chính thì mờ đi, ngược lại giữ text sáng
                    color: i === j ? '#94a3b8' : '#f8fafc',
                  }}>
                    {val.toFixed(2)}
                  </td>
                )
              })}
            </tr>
          ))}
        </tbody>
      </table>
      <div style={{ display: 'flex', justifyContent: 'center', gap: 24, marginTop: 14, fontSize: 11, color: '#94a3b8' }}>
        <span style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
          <span style={{ width: 32, height: 10, background: 'rgba(59,130,246,0.7)', borderRadius: 3, display: 'inline-block' }} />
          Tương quan nghịch
        </span>
        <span style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
          <span style={{ width: 32, height: 10, background: 'rgba(239,68,68,0.7)', borderRadius: 3, display: 'inline-block' }} />
          Tương quan thuận
        </span>
      </div>
    </div>
  )
}