import ChartCard from '../components/ChartCard'
import SalesTrendLine from '../components/charts/SalesTrendLine'
import { HourlyChart, WeekdayChart } from '../components/charts/TemporalCharts'
import TimeHeatmap from '../components/charts/TimeHeatmap'

export default function TemporalPage() {
  return (
    <div className="fade-up">
      <div className="page-header">
        <h1>📅 Phân tích xu hướng thời gian</h1>
        <p>Hành vi mua sắm theo ngày, giờ và thứ trong tuần</p>
      </div>

      <div className="charts-grid">
        <ChartCard
          title="Xu hướng đơn hàng theo ngày"
          subtitle="Daily sales trend — Oct 2019 đến Feb 2020"
          badge="Time Series"
        >
          <SalesTrendLine />
          <div style={{ marginTop: 10, fontSize: 12, color: '#475569' }}>
            💡 Điểm đỉnh tại Black Friday (cuối tháng 11) với mức tăng ~90% so với ngày thường.
          </div>
        </ChartCard>

        <div className="charts-grid grid-2">
          <ChartCard title="Mua sắm theo giờ trong ngày" subtitle="Tổng đơn hàng theo từng khung giờ (0–23h)">
            <HourlyChart />
            <div style={{ marginTop: 8, fontSize: 12, color: '#475569' }}>
              💡 Đỉnh mua sắm lúc 20h–21h.
            </div>
          </ChartCard>

          <ChartCard title="Mua sắm theo thứ trong tuần" subtitle="Thứ 7 và Chủ nhật dẫn đầu">
            <WeekdayChart />
            <div style={{ marginTop: 8, fontSize: 12, color: '#475569' }}>
              💡 Weekend cao hơn 35% so với ngày thường.
            </div>
          </ChartCard>
        </div>

        <ChartCard
          title="Bản đồ nhiệt: Mật độ mua sắm"
          subtitle="Thứ × Giờ — màu càng đậm = càng nhiều đơn"
          badge="Heatmap"
        >
          <TimeHeatmap />
          <div style={{ marginTop: 12, fontSize: 12, color: '#475569' }}>
            💡 Khung giờ vàng: Thứ 7 lúc 19h–21h có mật độ đơn hàng cao nhất.
          </div>
        </ChartCard>
      </div>
    </div>
  )
}
