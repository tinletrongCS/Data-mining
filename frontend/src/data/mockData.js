// ============================================================
// MOCK DATA — Jewelry E-Commerce Dataset
// Schema mirrors actual data from data/processed/*.pkl
// ============================================================

// ——— KPI TỔNG QUAN ———
export const kpiData = {
  totalOrders: 284921,
  totalRevenue: 18472350,
  uniqueCustomers: 51823,
  avgOrderValue: 64.83,
  totalProducts: 3291,
  dateRange: 'Oct 2019 – Feb 2020',
}

// ——— PHÂN PHỐI GIÁ (Histogram log-scale) ———
export const priceDistribution = [
  { bin: '$1', count: 180 }, { bin: '$5', count: 420 },
  { bin: '$10', count: 1850 }, { bin: '$20', count: 3200 },
  { bin: '$30', count: 8400 }, { bin: '$50', count: 15600 },
  { bin: '$75', count: 22800 }, { bin: '$100', count: 31200 },
  { bin: '$150', count: 28500 }, { bin: '$200', count: 24100 },
  { bin: '$300', count: 18700 }, { bin: '$500', count: 9800 },
  { bin: '$750', count: 5200 }, { bin: '$1K', count: 2800 },
  { bin: '$1.5K', count: 1400 }, { bin: '$2K', count: 820 },
  { bin: '$3K', count: 380 }, { bin: '>$5K', count: 140 },
]

// ——— TOP 10 DANH MỤC ———
export const topCategories = [
  { name: 'Nhẫn (Ring)', count: 52840 },
  { name: 'Vòng cổ (Necklace)', count: 44320 },
  { name: 'Bông tai (Earring)', count: 38910 },
  { name: 'Vòng tay (Bracelet)', count: 34220 },
  { name: 'Mặt dây (Pendant)', count: 28450 },
  { name: 'Lắc chân (Anklet)', count: 18300 },
  { name: 'Trâm cài (Brooch)', count: 12100 },
  { name: 'Mắt đá (Stud)', count: 10800 },
  { name: 'Dây chuyền (Chain)', count: 9200 },
  { name: 'Charm', count: 7600 },
]

// ——— TOP 10 THƯƠNG HIỆU ———
export const topBrands = [
  { name: 'Pandora', count: 38420 },
  { name: 'Swarovski', count: 29840 },
  { name: 'Tiffany & Co.', count: 24100 },
  { name: 'Cartier', count: 18750 },
  { name: 'Zales', count: 16200 },
  { name: 'Kay Jewelers', count: 14800 },
  { name: 'Signet', count: 12500 },
  { name: 'Stuller', count: 10300 },
  { name: 'Kendra Scott', count: 9800 },
  { name: 'Gorjana', count: 8200 },
]

// ——— MA TRẬN TƯƠNG QUAN ———
export const correlationData = {
  labels: ['price', 'quantity', 'hour', 'weekday', 'recency'],
  matrix: [
    [1.00,  0.12,  0.03, -0.07,  0.23],
    [0.12,  1.00, -0.04,  0.02, -0.08],
    [0.03, -0.04,  1.00,  0.15, -0.02],
    [-0.07, 0.02,  0.15,  1.00,  0.11],
    [0.23, -0.08, -0.02,  0.11,  1.00],
  ],
}

// ——— XU HƯỚNG DOANH SỐ THEO NGÀY ———
const buildSalesTrend = () => {
  const data = []
  const start = new Date('2019-10-01')
  for (let i = 0; i < 150; i++) {
    const d = new Date(start); d.setDate(start.getDate() + i)
    const dw = d.getDay()
    const weekend = dw === 0 || dw === 6 ? 1.3 : 1.0
    const bf = i >= 57 && i <= 62 ? 1.9 : 1.0
    const trend = 1 + i * 0.003
    const noise = 0.82 + Math.random() * 0.32
    data.push({
      date: d.toISOString().split('T')[0],
      orders: Math.round(780 * weekend * trend * noise * bf),
      label: d.toLocaleDateString('vi-VN', { month: 'short', day: 'numeric' }),
    })
  }
  return data
}
export const salesTrend = buildSalesTrend()

// ——— MUA SẮM THEO GIỜ ———
export const hourlyOrders = [
  {h:0,v:1240},{h:1,v:820},{h:2,v:480},{h:3,v:310},{h:4,v:280},{h:5,v:520},
  {h:6,v:1640},{h:7,v:3420},{h:8,v:5800},{h:9,v:8920},{h:10,v:12400},{h:11,v:14200},
  {h:12,v:13800},{h:13,v:11200},{h:14,v:10800},{h:15,v:11800},{h:16,v:13200},{h:17,v:14800},
  {h:18,v:16200},{h:19,v:17400},{h:20,v:18200},{h:21,v:16800},{h:22,v:12400},{h:23,v:6800},
]

// ——— MUA SẮM THEO THỨ ———
export const weekdayOrders = [
  { day: 'Thứ 2', orders: 36420 },
  { day: 'Thứ 3', orders: 34820 },
  { day: 'Thứ 4', orders: 36100 },
  { day: 'Thứ 5', orders: 38200 },
  { day: 'Thứ 6', orders: 42800 },
  { day: 'Thứ 7', orders: 51200 },
  { day: 'CN',    orders: 47400 },
]

// ——— HEATMAP: THỨ × GIỜ ———
const hm = {
  'Thứ 2': [12,8,4,3,3,5,16,34,58,89,100,95,88,76,72,78,88,92,98,100,96,84,62,36],
  'Thứ 3': [11,7,4,3,3,5,15,33,56,87,98,93,86,74,70,76,86,90,96,98,94,82,60,34],
  'Thứ 4': [12,8,4,3,3,5,16,34,58,89,100,95,88,76,72,78,88,92,98,100,96,84,62,36],
  'Thứ 5': [14,9,5,3,3,6,18,36,60,91,102,97,90,78,74,80,90,94,100,102,98,86,64,38],
  'Thứ 6': [18,12,6,4,4,7,22,42,70,98,112,108,100,86,82,88,100,108,114,116,112,96,72,44],
  'Thứ 7': [24,16,10,6,6,10,28,52,86,118,138,132,122,106,100,108,122,132,138,142,136,116,88,54],
  'CN':    [20,14,8,5,5,8,24,46,78,108,126,120,112,96,92,98,112,120,126,130,124,106,80,48],
}
export const timeHeatmapData = Object.entries(hm).map(([day, values]) => ({
  day, values: values.map((v, h) => ({ hour: h, value: v })),
}))

// ——— SCATTER PHÂN CỤM ———
const mkPoints = (cluster, n, rR, oR, sR) =>
  Array.from({ length: n }, () => {
    const r = rR[0] + Math.random() * (rR[1] - rR[0])
    const o = oR[0] + Math.random() * (oR[1] - oR[0])
    const s = sR[0] + Math.random() * (sR[1] - sR[0])
    return { cluster, x: +Math.log1p(r).toFixed(3), y: +Math.log1p(o).toFixed(3),
      recency: Math.round(r), total_orders: Math.round(o), avg_order_value: Math.round(s) }
  })

export const clusterScatter = [
  ...mkPoints(0, 160, [45,130], [1,4],  [10,80]),
  ...mkPoints(1, 130, [20,55],  [4,12], [40,120]),
  ...mkPoints(2, 110, [8,28],   [10,25],[80,200]),
  ...mkPoints(3,  60, [2,12],   [20,60],[150,500]),
]

// ——— PROFILE CỤM ———
export const clusterProfiles = [
  { id:0, name:'At Risk',   nameVi:'Rời bỏ',   color:'#ef4444', recency:82, total_orders:2.3, avg_order_value:50, user_count:18320 },
  { id:1, name:'Regular',   nameVi:'Thông thường', color:'#22c55e', recency:35, total_orders:7.8, avg_order_value:50, user_count:15840 },
  { id:2, name:'Loyal',     nameVi:'Trung thành', color:'#eab308', recency:15, total_orders:16, avg_order_value:51, user_count:12640 },
  { id:3, name:'VIP',       nameVi:'VIP',       color:'#3b82f6', recency:6,  total_orders:38, avg_order_value:100, user_count:5023 },
]

// ——— ELBOW CHART ———
export const elbowData = [
  {k:1,wcss:142800},{k:2,wcss:89420},{k:3,wcss:61200},{k:4,wcss:44800},
  {k:5,wcss:40200},{k:6,wcss:37800},{k:7,wcss:36100},{k:8,wcss:35200},
  {k:9,wcss:34600},{k:10,wcss:34200},
]

// ——— SILHOUETTE SCORE ———
export const silhouetteData = [
  {k:2,score:0.312},{k:3,score:0.387},{k:4,score:0.428},{k:5,score:0.401},
  {k:6,score:0.376},{k:7,score:0.354},{k:8,score:0.341},{k:9,score:0.329},{k:10,score:0.318},
]

// ——— RFM RADAR ———
export const rfmRadarData = [
  { cluster:'At Risk',   recency:0.12, frequency:0.08, monetary:0.10 },
  { cluster:'Regular',   recency:0.45, frequency:0.28, monetary:0.18 },
  { cluster:'Loyal',     recency:0.72, frequency:0.58, monetary:0.42 },
  { cluster:'VIP',       recency:0.92, frequency:0.98, monetary:1.00 },
]

// ——— CLUSTER MEAN STATS (bar comparison) ———
export const clusterMeans = {
  recency:         [82, 35, 15, 6],
  total_orders:    [2, 8, 16, 38],
  total_spend:     [115, 392, 824, 3841],
  avg_order_value: [50, 50, 51, 100],
}

// ——— SO SÁNH TRƯỚC/SAU XỬ LÝ ———
export const preprocessComparison = {
  before: [
    {bin:'$0',c:42000},{bin:'$100',c:85000},{bin:'$200',c:22000},
    {bin:'$500',c:8000},{bin:'$1K',c:2800},{bin:'$2K',c:820},
    {bin:'$5K',c:180},{bin:'>$10K',c:42},
  ],
  after: [
    {bin:'$10',c:3200},{bin:'$30',c:8400},{bin:'$50',c:22800},
    {bin:'$75',c:31200},{bin:'$100',c:28500},{bin:'$150',c:18700},
    {bin:'$200',c:12800},{bin:'$300',c:7400},{bin:'<$413',c:2200},
  ],
}
