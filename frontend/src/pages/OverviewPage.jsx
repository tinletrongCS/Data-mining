import StatCard from '../components/StatCard'
import ChartCard from '../components/ChartCard'
import PriceHistogram from '../components/charts/PriceHistogram'
import TopCategoriesBar from '../components/charts/TopCategoriesBar'
import { kpiData, topCategories, topBrands } from '../data/mockData'

export default function OverviewPage() {
  return (
    <div className="fade-up">
      <div className="page-header">
        <h1>📊 Tổng quan dữ liệu</h1>
        <p>Phân tích tổng hợp dataset Jewelry E-Commerce · {kpiData.dateRange}</p>
      </div>

      <div className="stats-grid">
        <StatCard icon="🛍️" label="Tổng đơn hàng" value={kpiData.totalOrders.toLocaleString()} sub="trong 5 tháng" />
        <StatCard icon="💰" label="Doanh thu" value={`$${(kpiData.totalRevenue/1e6).toFixed(2)}M`} sub="USD" />
        <StatCard icon="👥" label="Khách hàng" value={kpiData.uniqueCustomers.toLocaleString()} sub="unique users" />
        <StatCard icon="🧾" label="AOV" value={`$${kpiData.avgOrderValue}`} sub="Avg Order Value" />
        <StatCard icon="💎" label="Sản phẩm" value={kpiData.totalProducts.toLocaleString()} sub="SKUs" />
      </div>

      <div className="charts-grid grid-2">
        <ChartCard
          title="Phân phối giá sản phẩm"
          subtitle="Histogram — thang đo Log Scale"
          badge="Log Scale"
          className="span-2"
        >
          <PriceHistogram />
          <div style={{ marginTop: 10, fontSize: 12, color: '#475569' }}>
            💡 Giá tập trung ở vùng $75–$200. Đuôi dài về phía phải cho thấy có một số sản phẩm cao cấp.
          </div>
        </ChartCard>

        <ChartCard title="Top 10 danh mục bán chạy" subtitle="Theo số lượng giao dịch">
          <TopCategoriesBar data={topCategories} />
        </ChartCard>

        <ChartCard title="Top 10 thương hiệu" subtitle="Theo số lượng giao dịch">
          <TopCategoriesBar data={topBrands} />
        </ChartCard>
      </div>
    </div>
  )
}
