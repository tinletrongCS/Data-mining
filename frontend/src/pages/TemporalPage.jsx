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
          subtitle="Daily sales trend from Dec 2018 to Dec 2021"
          badge="Time Series"
        >
          <SalesTrendLine />

        </ChartCard>

        <div className="charts-grid grid-2">
          <ChartCard title="Mua sắm theo giờ trong ngày" subtitle="Tổng đơn hàng theo từng khung giờ (0–23h)">
            <HourlyChart />

          </ChartCard>

          <ChartCard title="Mua sắm theo thứ trong tuần" subtitle="Thứ 5 dẫn đầu">
            <WeekdayChart />
          </ChartCard>
        </div>

        <ChartCard
          title="Bản đồ nhiệt: Mật độ mua sắm"
          subtitle="Thứ × Giờ — màu càng đậm càng nhiều đơn"
          badge="Heatmap"
        >
          <TimeHeatmap />

        </ChartCard>
      </div>
    </div>
  )
}
