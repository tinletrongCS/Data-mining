import ChartCard from '../components/ChartCard'
import CorrelationHeatmap from '../components/charts/CorrelationHeatmap'
import PreprocessChart from '../components/charts/PreprocessChart'

export default function ComparisonPage() {
  return (
    <div className="fade-up">
      <div className="page-header">
        <h1>⚖️ So sánh & Phân tích tương quan</h1>
        <p>Tiền xử lý dữ liệu và ma trận tương quan giữa các biến số</p>
      </div>

      <div className="charts-grid">
        <ChartCard
          title="So sánh trước và sau tiền xử lý"
          subtitle="Phân phối giá sản phẩm — loại bỏ outlier và chuẩn hóa"
          badge="Preprocessing"
        >
          <PreprocessChart />
          <div style={{ marginTop: 14, padding: '12px 16px', background: 'rgba(0,212,255,0.05)', borderRadius: 8, border: '1px solid rgba(0,212,255,0.15)', fontSize: 12, color: '#94a3b8', lineHeight: 1.7 }}>
            <strong style={{ color: '#00d4ff' }}>Quy trình xử lý:</strong>
            <ul style={{ paddingLeft: 18, marginTop: 6 }}>
              <li>Loại bỏ giá trị null và giá = 0</li>
              <li>Cắt outlier tại ngưỡng 99th percentile (~$413)</li>
              <li>Log transformation để giảm độ lệch phân phối</li>
              <li>MinMax Scaling cho các feature đầu vào KMeans</li>
            </ul>
          </div>
        </ChartCard>

        <ChartCard
          title="Ma trận tương quan giữa các biến số"
          subtitle="Pearson correlation — chỉ các biến số (loại bỏ ID)"
          badge="Heatmap"
        >
          <CorrelationHeatmap />
          <div style={{ marginTop: 14, display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12 }}>
            {[
              { pair: 'price ↔ recency', val: '0.23', note: 'Khách mua hàng đắt thường quay lại lâu hơn' },
              { pair: 'hour ↔ weekday', val: '0.15', note: 'Giờ mua phụ thuộc nhẹ vào ngày trong tuần' },
              { pair: 'price ↔ quantity', val: '0.12', note: 'Mua nhiều hơn khi giá thấp hơn' },
              { pair: 'weekday ↔ recency', val: '0.11', note: 'Xu hướng mua theo ngày' },
            ].map(item => (
              <div key={item.pair} style={{ padding: '10px 12px', background: 'rgba(255,255,255,0.03)', borderRadius: 8, border: '1px solid rgba(255,255,255,0.06)' }}>
                <div style={{ fontSize: 12, fontWeight: 600, color: '#00d4ff' }}>{item.pair} = {item.val}</div>
                <div style={{ fontSize: 11, color: '#64748b', marginTop: 3 }}>{item.note}</div>
              </div>
            ))}
          </div>
        </ChartCard>
      </div>
    </div>
  )
}
