import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from collections import Counter

class KMeansSegmentation:
    def __init__(self, df: pd.DataFrame):
        self.df_processed = df.copy()
        self.model = None
        self.df_scaled = None
        self.scaler = StandardScaler()

        # cac thuoc tinh RFM can cho k means
        self.rfm_attributes = ['recency', 'total_orders', 'total_spend', 'avg_order_value']

    def preprocess(self):
        """
        Chuẩn hóa dữ liệu
        Log transformation
        """
        # X = self.df_processed[self.rfm_attributes]
        # self.df_scaled = pd.DataFrame(self.scaler.fit_transform(X), columns=self.rfm_attributes)
        # return self.df_scaled
        # 1. ÁP DỤNG LOG TRANSFORM CHO CÁC CỘT TIỀN VÀ SỐ LƯỢNG (Bí kíp chống lệch Centroid)
        # Dùng log1p (log(1+x)) để tránh lỗi khi giá trị = 0
        df_rfm = self.df_processed[['recency', 'total_orders', 'total_spend', 'avg_order_value']].copy()
        df_rfm['total_spend_log'] = np.log1p(df_rfm['total_spend'])
        df_rfm['avg_order_value_log'] = np.log1p(df_rfm['avg_order_value'])
        df_rfm['total_orders_log'] = np.log1p(df_rfm['total_orders'])

        features_to_scale = ['recency', 'total_orders_log', 'total_spend_log', 'avg_order_value_log']
        scaler = StandardScaler()
        self.df_scaled = pd.DataFrame(scaler.fit_transform(df_rfm[features_to_scale]), columns=features_to_scale)

        return self.df_scaled

    def train(self, n_clusters=4):
        """
        Huấn luyện K-Means với số cụm K chỉ định.
        """
        if self.df_scaled is None:
            self.df_scaled = self.preprocess()
        self.model = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        self.model.fit(self.df_scaled)
        self.df_processed['cluster'] = self.model.labels_
        return self.df_processed


    def profile_clusters(self):
        """
        Phân tích đặc điểm của từng cụm
        """
        if 'cluster' not in self.df_processed.columns:
            print("Vui lòng gọi hàm train() trước khi phân tích!")
            return None

        # Thống kê trung bình các chỉ số RFM
        summary = self.df_processed.groupby('cluster')[self.rfm_attributes].mean().round(2)
        summary['user_count'] = self.df_processed['cluster'].value_counts()

        # Tìm loại đá quý (gem) yêu thích nhất của từng cụm
        top_gems = []
        for cluster_id in summary.index:
            # Lấy tất cả list đá quý của cụm này
            cluster_gems = self.df_processed[self.df_processed['cluster'] == cluster_id]['favorite_gems']

            # Gom tất cả list lại thành 1 list
            all_gems_in_cluster = []
            for gem_list in cluster_gems:
                if isinstance(gem_list, list):
                    all_gems_in_cluster.extend(gem_list)

            # Đếm xem đá nào xuất hiện nhiều nhất
            if all_gems_in_cluster:
                most_common = Counter(all_gems_in_cluster).most_common(5)  # Lấy top 2
                top_gems.append([gem for gem, count in most_common if gem != 'unknown'])
            else:
                top_gems.append([])

        summary['top_favorite_gems'] = top_gems

        return summary