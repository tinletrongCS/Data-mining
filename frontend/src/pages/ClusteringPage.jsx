import ChartCard from '../components/ChartCard'
import ElbowChart from '../components/charts/ElbowChart'
import SilhouetteChart from '../components/charts/SilhouetteChart'
import ClusterScatterChart from '../components/charts/ClusterScatter'
import RFMRadarChart from '../components/charts/RFMRadarChart'
import ClusterBarComparison from '../components/charts/ClusterBarComparison'
import { clusterProfiles } from '../data/mockData'

const PROFILE_ICONS = ['⚠️','🟢','⭐','👑']

export default function ClusteringPage() {
  return (
    <div className="fade-up">
      <div className="page-header">
        <h1>🔮 Phân cụm khách hàng — KMeans</h1>
        <p>Phân tích RFM và phân khúc khách hàng thành 4 nhóm với K=4 tối ưu</p>
      </div>

      {/* Cluster profile cards */}
      <div className="cluster-cards">
        {clusterProfiles.map((p, i) => (
          <div key={p.id} className="cluster-card">
            <div className="cluster-card-bar" style={{ background: p.color }} />
            <div style={{ fontSize: 20, marginBottom: 8 }}>{PROFILE_ICONS[i]}</div>
            <div className="cluster-card-name">{PROFILE_ICONS[i]} {p.nameVi}</div>
            <div className="cluster-card-sub">{p.user_count.toLocaleString()} khách hàng</div>
            <div className="cluster-stat">Recency <span>{p.recency} ngày</span></div>
            <div className="cluster-stat">Đơn hàng <span>{p.total_orders}</span></div>
            <div className="cluster-stat">AOV <span>${p.avg_order_value}</span></div>
          </div>
        ))}
      </div>

      <div className="charts-grid grid-2">
        <ChartCard title="Phương pháp Elbow" subtitle="WCSS giảm dần — điểm uốn tại K=4" badge="Elbow Method">
          <ElbowChart />
        </ChartCard>

        <ChartCard title="Hệ số Silhouette" subtitle="Đánh giá chất lượng phân cụm theo K" badge="Silhouette">
          <SilhouetteChart />
        </ChartCard>

        <ChartCard title="Phân bố cụm trong không gian 2D" subtitle="Log(Recency) vs Log(Total Orders)" badge="Scatter Plot" className="span-2">
          <ClusterScatterChart />
        </ChartCard>

        <ChartCard title="Hồ sơ RFM theo cụm" subtitle="Radar Chart — so sánh 3 trục R-F-M" badge="Radar">
          <RFMRadarChart />
        </ChartCard>

        <ChartCard title="So sánh chỉ số RFM giữa các cụm" subtitle="Giá trị trung bình theo từng chỉ số">
          <ClusterBarComparison />
        </ChartCard>
      </div>
    </div>
  )
}
