import ChartCard from '../components/ChartCard'
import ElbowChart from '../components/charts/ElbowChart'
import SilhouetteChart from '../components/charts/SilhouetteChart'
import ClusterScatterChart from '../components/charts/ClusterScatter'
import RFMRadarChart from '../components/charts/RFMRadarChart'
import ClusterBarComparison from '../components/charts/ClusterBarComparison'
import { clusterProfiles } from '../data/mockData'

// Định nghĩa Metadata để tự động gán nhãn và màu sắc dựa trên tên cụm từ dữ liệu
const CLUSTER_META = {
  'VIP':       { icon: '👑', color: '#3b82f6', nameVi: 'VIP' },
  'Loyal':     { icon: '⭐', color: '#eab308', nameVi: 'Loyal' },
  'Regular':   { icon: '🟢', color: '#22c55e', nameVi: 'Regular' },
  'At Risk':   { icon: '⚠️', color: '#ef4444', nameVi: 'At Risk' },
};

export default function ClusteringPage() {
  return (
    <div className="fade-up">
      <div className="page-header">
        <h1>🔮 Phân cụm khách hàng — KMeans</h1>
        <p>Phân tích RFM và phân khúc khách hàng thành 4 nhóm với K=4 tối ưu</p>
      </div>

      {/* Cluster profile cards */}
      <div className="cluster-cards">
        {clusterProfiles.map((p) => {
          // Lấy metadata dựa trên tên tiếng Anh (VIP, Loyal...) được Python gán
          const meta = CLUSTER_META[p.name] || { icon: '❓', color: '#94a3b8', nameVi: 'Chưa xác định' };
          
          return (
            <div key={p.id} className="cluster-card">
              {/* Sử dụng màu sắc từ CLUSTER_META */}
              <div className="cluster-card-bar" style={{ background: meta.color }} />
              
              <div style={{ fontSize: 24, marginBottom: 8 }}>{meta.icon}</div>
              
              <div className="cluster-card-name" style={{ color: meta.color, fontWeight: 'bold' }}>
                {meta.nameVi}
              </div>
              
              <div className="cluster-card-sub">{p.user_count.toLocaleString()} khách hàng</div>
              
              <div className="cluster-stat">Recency <span>{p.recency} ngày</span></div>
              <div className="cluster-stat">Đơn hàng <span>{p.total_orders}</span></div>
              <div className="cluster-stat">AOV <span>${p.avg_order_value}</span></div>
            </div>
          );
        })}
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