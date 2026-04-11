import dashboardData from './dashboard_data.json';

// Export TOÀN BỘ dữ liệu từ JSON ra cho App React sử dụng
export const {
  kpiData,
  priceDistribution,
  topCategories,
  topBrands,
  correlationData,
  salesTrend,
  hourlyOrders,
  weekdayOrders,
  timeHeatmapData,
  clusterScatter,
  clusterProfiles,
  rfmRadarData,
  clusterMeans,
  elbowData,              // Đã có từ JSON
  silhouetteData,         // Đã có từ JSON
  preprocessComparison    // Đã có từ JSON
} = dashboardData;