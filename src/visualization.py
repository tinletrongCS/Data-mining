import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import MinMaxScaler
# Cấu hình giao diện biểu đồ cho đẹp (chuẩn báo cáo khoa học)
sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

def save(save_path):
    plt.savefig(save_path, bbox_inches='tight')
    print(f"Đã lưu biểu đồ tại: {save_path}")

def plot_price_distribution(df: pd.DataFrame, save_path=None):
    """
    TODO - Vẽ biểu đồ phân phối giá (Histogram + KDE).
    TODO - Giúp nhận biết mức giá phổ biến và phát hiện Outlier giá cao.
    """
    plt.figure(figsize=(12, 6))

    # Vẽ Histogram kết hợp KDE
    sns.histplot(df['price'], bins=50, kde=True, color='teal', log_scale=True)

    plt.title('Phân phối giá sản phẩm (Log Scale)', fontsize=15, fontweight='bold')
    plt.xlabel('Giá (USD) - Thang đo Log', fontsize=12)
    plt.ylabel('Số lượng sản phẩm', fontsize=12)

    if save_path:
        save(save_path)
    plt.show()


def plot_top_categories(df: pd.DataFrame, column, top_n=10, save_path=None):
    """
    TODO - Vẽ biểu đồ Top các danh mục/thương hiệu phổ biến nhất.
    """
    plt.figure(figsize=(12, 6))

    # Đếm số lượng và lấy Top N
    top_data = df[column].value_counts().nlargest(top_n).reset_index()
    top_data.columns = [column, 'count']
    sns.barplot(data=top_data, x='count', y=column, palette='viridis', hue=column, legend=False)

    plt.title(f'Top {top_n} {column} bán chạy nhất', fontsize=15, fontweight='bold')
    plt.xlabel('Số lượng giao dịch', fontsize=12)
    plt.ylabel(column, fontsize=12)

    if save_path:
        save(save_path)
    plt.show()


def plot_correlation_heatmap(df: pd.DataFrame, save_path=None):
    """
    TODO - Vẽ biểu đồ nhiệt thể hiện sự tương quan giữa các biến SỐ
    """
    # Chỉ lấy các cột số (loại bỏ cột string như 'jewelry.gold')
    numeric_df = df.select_dtypes(include=[np.number])

    # Loại bỏ các cột ID vì ID là số ngẫu nhiên, không có ý nghĩa tương quan
    cols_to_drop = ['order_id', 'product_id', 'user_id', 'category_id', 'brand_id']
    numeric_df = numeric_df.drop(columns=[col for col in cols_to_drop if col in numeric_df.columns])

    if numeric_df.empty or numeric_df.shape[1] < 2:
        print("Không đủ dữ liệu số để vẽ tương quan (Cần ít nhất 2 cột số: price, quantity, hour...).")
        return

    plt.figure(figsize=(10, 8))

    # Tính ma trận tương quan
    corr = numeric_df.corr()

    # Vẽ Heatmap
    mask = np.triu(np.ones_like(corr, dtype=bool))  # Che một nửa tam giác trên cho gọn
    sns.heatmap(corr, mask=mask, annot=True, fmt=".2f", cmap='coolwarm', vmin=-1, vmax=1, linewidths=0.5)

    plt.title('Ma trận tương quan giữa các biến số', fontsize=15, fontweight='bold')

    if save_path:
        save(save_path)
    plt.show()


def plot_preprocessing_comparison(df_raw: pd.DataFrame, df_clean: pd.DataFrame, save_path=None):
    """
    TODO Vẽ biểu đồ so sánh trước và sau khi thực hiện tiền xử lý
    """
    fig, axes = plt.subplots(1, 2, figsize=(18, 6))

    raw_price = pd.to_numeric(df_raw['price'], errors='coerce').fillna(0)
    sns.histplot(raw_price, bins=50, ax=axes[0], color='gray')
    axes[0].set_title('Trước xử lý: Dữ liệu bị lệch (Skewed)', fontsize=14, color='red')
    axes[0].set_xlabel('Giá (USD)')
    axes[0].set_ylabel('Số lượng')


    if 'price' in df_clean.columns:
        limit_99 = df_clean['price'].quantile(0.99)
        df_visual = df_clean[df_clean['price'] <= limit_99]

        sns.histplot(df_visual['price'], bins=50, kde=True, ax=axes[1], color='teal')

        axes[1].set_title(f'Sau xử lý: Phân phối giá (Zoom vào vùng < {int(limit_99)}$)', fontsize=14, color='green')
        axes[1].set_xlabel('Giá (USD)')
        axes[1].set_ylabel('Số lượng')

    if save_path:
        save(save_path)
    plt.tight_layout()
    plt.show()


# TODO - BIỂU ĐÔ DÙNG PHÂN TÍCH XU HƯỚNG MUA HÀNG DỰA TRÊN DỮ LIỆU THỜI GIAN
def plot_sales_trend(df: pd.DataFrame, freq='D', save_path=None):
    """
    TODO - Vẽ xu hướng số lượng đơn hàng theo thời gian (Ngày/Tuần/Tháng).
        freq: 'D' (Ngày), 'W' (Tuần), 'M' (Tháng).
    """
    # Gom nhóm theo thời gian
    # set_index để dùng resample (mạnh hơn groupby cho time series)
    sales_trend = df.set_index('event_time').resample(freq)['order_id'].count()

    plt.figure(figsize=(15, 6))
    sales_trend.plot(kind='line', color='darkorange', linewidth=2, marker='o', markersize=4)

    freq_name = {'D': 'Ngày', 'W': 'Tuần', 'ME': 'Tháng'}
    plt.title(f'Xu hướng số lượng đơn hàng theo {freq_name.get(freq, freq)}', fontsize=15, fontweight='bold')
    plt.xlabel('Thời gian')
    plt.ylabel('Số lượng đơn hàng')
    plt.grid(True, linestyle='--', alpha=0.6)

    if save_path:
        save(save_path)
    plt.show()

def plot_temporal_trends(df: pd.DataFrame, save_path=None):
    """
    Vẽ biểu đồ xu hướng mua sắm theo giờ trong ngày và thứ trong tuần.
    Đầu vào là DataFrame đã chạy qua hàm extract_time_features.
    """
    sns.set_theme(style="whitegrid")
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))

    hourly_orders = df.groupby('hour')['order_id'].nunique().reset_index()
    hourly_orders.columns = ['Giờ trong ngày', 'Số lượng đơn hàng']
    
    sns.lineplot(
        data=hourly_orders, 
        x='Giờ trong ngày', 
        y='Số lượng đơn hàng', 
        ax=axes[0], 
        marker='o',       # Thêm chấm tròn tại các điểm
        color='#1f77b4',  # Màu xanh dương chuẩn
        linewidth=2.5
    )
    axes[0].set_title('Xu hướng Mua sắm theo Giờ trong ngày', fontsize=14, fontweight='bold')
    axes[0].set_xticks(range(0, 24, 2)) # Hiện trục X chẵn 2, 4, 6...22
    axes[0].set_xlabel('Giờ (0 - 23)', fontsize=12)
    axes[0].set_ylabel('Tổng số đơn hàng', fontsize=12)
    
    # ==========================================
    # 2. BIỂU ĐỒ CỘT: XU HƯỚNG THEO THỨ (WEEKDAY)
    # ==========================================
    # Đếm số lượng đơn hàng theo thứ
    weekday_orders = df.groupby('weekday_name')['order_id'].nunique().reset_index()
    weekday_orders.columns = ['Thứ trong tuần', 'Số lượng đơn hàng']
    
    # Ép kiểu Categorical để thứ tự các ngày hiển thị đúng từ Thứ 2 đến Chủ nhật
    days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    weekday_orders['Thứ trong tuần'] = pd.Categorical(weekday_orders['Thứ trong tuần'], categories=days_order, ordered=True)
    weekday_orders = weekday_orders.sort_values('Thứ trong tuần')
    
    sns.barplot(
        data=weekday_orders, 
        x='Thứ trong tuần', 
        y='Số lượng đơn hàng', 
        ax=axes[1], 
        palette='viridis' # Dải màu đẹp mắt
    )
    axes[1].set_title('Xu hướng Mua sắm theo Thứ trong tuần', fontsize=14, fontweight='bold')
    axes[1].set_xlabel('Thứ', fontsize=12)
    axes[1].set_ylabel('Tổng số đơn hàng', fontsize=12)
    axes[1].tick_params(axis='x', rotation=45) # Xoay chữ ở trục X cho dễ nhìn
    
    # Khoảng cách giữa 2 biểu đồ
    if (save_path):
        save(save_path)
    plt.tight_layout()
    plt.show()

def plot_sales_by_weekday(df: pd.DataFrame, save_path=None):
    """
    TODO - Vẽ biểu đồ cột thống kê tổng lượng đơn hàng theo 7 ngày trong tuần.
        Giúp nhận diện "Ngày vàng" trong tuần (Ví dụ: Thứ 7 hay Chủ Nhật?).
    """
    # Kiểm tra xem đã chạy Phase 2 (tạo cột thứ) chưa
    if 'weekday_name' not in df.columns:
        print("Lỗi: Thiếu cột 'weekday_name'. Hãy chạy hàm extract_time_features trước.")
        return

    # 1. Gom nhóm và đếm số lượng đơn hàng
    # Dùng nunique để đếm số đơn hàng duy nhất (tránh đếm trùng sản phẩm trong 1 đơn)
    weekday_counts = df.groupby('weekday_name')['order_id'].nunique()

    # 2. Sắp xếp lại thứ tự từ Thứ 2 -> Chủ Nhật cho đúng chuẩn
    days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    # Chỉ lấy những ngày có trong dữ liệu và sắp xếp theo list mẫu
    weekday_counts = weekday_counts.reindex(days_order).dropna()

    # 3. Vẽ biểu đồ
    plt.figure(figsize=(10, 6))

    # Vẽ cột màu xanh (SkyBlue), thêm viền đen cho rõ
    ax = weekday_counts.plot(kind='bar', color='skyblue', edgecolor='black', zorder=3)

    plt.title('Thống kê lượng đơn hàng theo ngày trong tuần', fontsize=15, fontweight='bold')
    plt.xlabel('Thứ trong tuần', fontsize=12)
    plt.ylabel('Tổng số đơn hàng', fontsize=12)
    plt.xticks(rotation=45)  # Xoay chữ cho dễ đọc
    plt.grid(axis='y', linestyle='--', alpha=0.7, zorder=0)  # Chỉ kẻ lưới ngang

    # Thêm số liệu trên đầu mỗi cột
    for i, v in enumerate(weekday_counts):
        ax.text(i, v + (v * 0.01), str(int(v)), ha='center', fontweight='bold')

    if save_path:
        plt.savefig(save_path, bbox_inches='tight')
    plt.show()

def plot_time_heatmap(df: pd.DataFrame, save_path=None):
    """
    TODO - Vẽ Heatmap thể hiện mật độ mua sắm theo: Thứ trong tuần vs Giờ trong ngày.
        Giúp tìm ra "Khung giờ vàng".
    """
    if 'weekday_name' not in df.columns or 'hour' not in df.columns:
        print("Lỗi: Thiếu cột 'weekday_name' hoặc 'hour'. Hãy chạy Phase 2 trước.")
        return

    # 1. Tạo bảng Pivot: Hàng=Thứ, Cột=Giờ, Giá trị=Số đơn
    # Thứ tự các thứ trong tuần để vẽ cho đúng chuẩn
    order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    pivot_table = df.pivot_table(
        index='weekday_name',
        columns='hour',
        values='order_id',
        aggfunc='count'
    ).reindex(order)  # Sắp xếp lại thứ tự thứ

    plt.figure(figsize=(16, 6))
    sns.heatmap(pivot_table, cmap='YlGnBu', annot=False, fmt='d', linewidths=0.5)

    plt.title('Bản đồ nhiệt: Mật độ mua sắm (Thứ vs Giờ)', fontsize=15, fontweight='bold')
    plt.xlabel('Giờ trong ngày (0-23h)')
    plt.ylabel('Thứ trong tuần')

    if save_path:
        save(save_path)
    plt.show()


# TODO: Biểu đồ phân cụm
def plot_cluster_boxplots(df_clustered: pd.DataFrame, save_path=None):
    """
    Vẽ biểu đồ Boxplot cho các chỉ số RFM theo từng cụm khách hàng.
    """
    # Các cột cần vẽ
    features = ['recency', 'total_orders', 'total_spend', 'avg_order_value']

    # Tạo khung hình 2x2
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('Đặc điểm RFM của các Cụm khách hàng (Boxplots)', fontsize=16, fontweight='bold')

    # Trải phẳng mảng axes để dễ lặp
    axes = axes.flatten()

    # Bảng màu đẹp cho các cụm
    palette = sns.color_palette("Set2", n_colors=df_clustered['cluster'].nunique())

    for i, feature in enumerate(features):
        sns.boxplot(
            x='cluster',
            y=feature,
            data=df_clustered,
            ax=axes[i],
            palette=palette,
            showfliers=False  # Ẩn bớt các điểm outlier quá xa để dễ nhìn
        )
        axes[i].set_title(f'Phân phối của {feature.upper()}', fontsize=12)
        axes[i].set_xlabel('Cụm (Cluster)')
        axes[i].set_ylabel('Giá trị')

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    if save_path:
        save(save_path)
    plt.show()

def plot_rfm_3d_scatter(df_clustered: pd.DataFrame, save_path=None):
    """
    Vẽ biểu đồ Scatter 3D thể hiện sự phân tách của các cụm trong không gian RFM.
    Đã fix lỗi dồn cục bằng cách dùng scale Logarit (np.log1p) và đồng bộ màu Radar.
    """
    fig = plt.figure(figsize=(12, 9))
    ax = fig.add_subplot(111, projection='3d')

    # 1. Đồng bộ màu sắc và tên gọi chính xác từ biểu đồ Radar Chart
    cluster_info = {
        0: {'label': 'Cụm 0', 'color': '#E74C3C'},          # Đỏ
        1: {'label': 'Cụm 1', 'color': '#27AE60'}, # Xanh lá
        2: {'label': 'Cụm 2', 'color': '#F1C40F'},        # Vàng
        3: {'label': 'Cụm 3', 'color': "#2B84DE"}       # Xanh biển
    }

    print("🔄 Đang vẽ biểu đồ 3D Scatter...")
    
    # 2. Thay đổi thứ tự vẽ (Vẽ các cụm đông người trước, cụm VIP/Cá mập ít người vẽ sau 
    # để các điểm VIP không bị đè khuất)
    draw_order = [3, 1, 0, 2] 

    for cluster_id in draw_order:
        if cluster_id not in df_clustered['cluster'].values:
            continue
            
        cluster_data = df_clustered[df_clustered['cluster'] == cluster_id]
        info = cluster_info.get(cluster_id, {'label': f'Cụm {cluster_id}', 'color': '#000000'})

        # 3. ÉP LOGARIT 3 TRỤC ĐỂ DỮ LIỆU BUNG ĐỀU RA (CHỐNG DỒN CỤC)
        x = np.log1p(cluster_data['recency'])
        y = np.log1p(cluster_data['total_orders'])
        z = np.log1p(cluster_data['avg_order_value'])

        ax.scatter(
            x, y, z,
            label=info['label'],
            alpha=0.7,            # Tăng độ trong suốt một chút để thấy các điểm bị chồng
            edgecolors='w',       # Viền trắng giúp các hạt tách bạch nhau hơn
            linewidth=0.5,
            s=60,                 # Tăng kích thước hạt lên một chút
            c=info['color']
        )

    # 4. Trang trí trục (Thêm labelpad để đẩy chữ ra)
    ax.set_xlabel('Log(Recency)', labelpad=10)
    ax.set_ylabel('Log(Total Orders)', labelpad=10)
    ax.set_zlabel('Log(Avg Order Value)', labelpad=25)
    ax.set_title('Phân bố 4 cụm Khách hàng trong không gian 3D (Log Scale)', fontsize=15, fontweight='bold', pad=25)

    # Hiển thị chú thích (Legend)
    ax.legend(title="Phân khúc khách hàng", bbox_to_anchor=(1.1, 0.9), loc='upper left', fontsize=11)
    
    # Xoay góc nhìn 3D
    ax.view_init(elev=20, azim=45) 

    fig.tight_layout()

    # 5. Lưu và hiển thị ảnh
    if save_path:
        save(save_path)
        
    plt.show()

def plot_elbow_method(df_scaled, max_k=10, optimal_k=4, save_path=None):
    """
    Hàm vẽ biểu đồ Khuỷu tay (Elbow) để chứng minh số cụm tối ưu.
    Tham số:
        - df_scaled: Dữ liệu đã qua chuẩn hóa StandardScaler (đầu ra của hàm preprocess).
        - max_k: Số lượng cụm tối đa muốn thử nghiệm (mặc định là 10).
        - optimal_k: Điểm K tối ưu để vẽ đường dóng màu đỏ nhấn mạnh.
    """
    wcss = []
    K_range = range(1, max_k + 1)
    
    print("🔄 Đang tính toán WCSS cho các giá trị K...")
    for k in K_range:
        # Chạy K-Means với từng giá trị K
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        kmeans.fit(df_scaled)
        
        # inertia_ chính là tổng bình phương khoảng cách từ các điểm đến tâm cụm (WCSS)
        wcss.append(kmeans.inertia_)
        
    plt.figure(figsize=(10, 6))
    sns.set_theme(style="whitegrid") # Giao diện lưới khoa học
    
    # Vẽ đường line chính
    sns.lineplot(x=K_range, y=wcss, marker='o', color='#2874A6', linewidth=2.5, markersize=8)
    
    # Thêm đường kẻ dọc đứt nét màu đỏ để nhấn mạnh K tối ưu
    if optimal_k in K_range:
        plt.axvline(x=optimal_k, color='red', linestyle='--', linewidth=2, 
                    label=f'Điểm khuỷu tay K = {optimal_k}')
        
        # Thêm text chú thích ngay tại điểm gập
        plt.text(optimal_k + 0.2, wcss[optimal_k-1], 'K tối ưu', color='red', fontsize=12, fontweight='bold')

    # Trang trí biểu đồ
    plt.title('Phương pháp Elbow giúp xác định số cụm tối ưu', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Số lượng phân khúc (K)', fontsize=12)
    plt.ylabel('Hàm mất mát WCSS (Inertia)', fontsize=12)
    plt.xticks(K_range) # Ép trục X hiện đủ các số nguyên từ 1 đến 10
    plt.legend()
    
    plt.tight_layout()
    if (save_path):
        save(save_path)
    plt.show()

def plot_silhouette_score(df_scaled, max_k=10, save_path=None):
    """
    Hàm vẽ biểu đồ Silhouette Score để đánh giá chất lượng phân cụm.
    Lưu ý: Tính toán Silhouette Score có độ phức tạp cao, nếu dữ liệu lớn (>50k dòng) sẽ hơi tốn thời gian.
    """
    silhouette_scores = []
    K_range = range(2, max_k + 1) # Bắt buộc chạy từ 2
    
    print("🔄 Đang tính toán Silhouette Score cho các giá trị K...")
    for k in K_range:
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        # Gán nhãn cho từng điểm dữ liệu
        cluster_labels = kmeans.fit_predict(df_scaled)
        
        # Tính điểm Silhouette trung bình cho toàn bộ tập dữ liệu
        score = silhouette_score(df_scaled, cluster_labels, sample_size=5000, random_state=42)
        silhouette_scores.append(score)
        print(f"✔️ K={k} | Silhouette Score: {score:.4f}")
        
    plt.figure(figsize=(10, 6))
    sns.set_theme(style="whitegrid")
    
    # Vẽ đường line chính (dùng màu xanh lá mạ cho khác biệt với Elbow)
    sns.lineplot(x=K_range, y=silhouette_scores, marker='s', color='#27AE60', linewidth=2.5, markersize=8)
    
    # Tìm giá trị K đạt điểm Silhouette cao nhất
    max_score = max(silhouette_scores)
    optimal_k = K_range[silhouette_scores.index(max_score)]
    
    # Thêm đường kẻ dọc đứt nét màu đỏ tại K đạt đỉnh
    plt.axvline(x=optimal_k, color='red', linestyle='--', linewidth=2, 
                label=f'K tối ưu (Điểm cao nhất) = {optimal_k}')
    
    # Thêm text chú thích ngay tại đỉnh
    plt.text(optimal_k + 0.2, max_score, f'Max: {max_score:.3f}', color='red', fontsize=12, fontweight='bold')

    # Trang trí biểu đồ
    plt.title('Hệ số Silhouette theo số cụm K', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Số cụm K', fontsize=12)
    plt.ylabel('Hệ số Silhouette', fontsize=12)
    plt.xticks(K_range) 
    plt.legend()
    
    plt.tight_layout()
    if (save_path):
        save(save_path)
    plt.show()


def plot_rfm_radar_chart(summary_df: pd.DataFrame, save_path=None):
    """
    Hàm vẽ biểu đồ Radar (Mạng nhện) so sánh 3 trục R-F-M của các phân khúc.
    Đã cập nhật: Sử dụng avg_order_value thay cho total_spend để tránh đa cộng tuyến.
    """
    # 1. Cập nhật rfm_cols: Dùng avg_order_value làm đại diện cho Monetary
    rfm_cols = ['recency', 'total_orders', 'avg_order_value']
    
    # Kiểm tra xem các cột này có thực sự tồn tại trong summary_df chưa
    for col in rfm_cols:
        if col not in summary_df.columns:
            print(f"Lỗi: Không tìm thấy cột '{col}' trong dữ liệu summary!")
            return

    # 2. Chuẩn hóa dữ liệu về thang [0, 1]
    scaler = MinMaxScaler()
    df_radar = pd.DataFrame(scaler.fit_transform(summary_df[rfm_cols]), columns=rfm_cols)
    
    # Nghịch đảo trục Recency (Càng thấp càng tốt -> Càng phình to trên Radar)
    df_radar['recency'] = 1 - df_radar['recency']
    
    # Đổi tên trục cho Radar Chart
    categories = ['Độ mới\n(recency)', 'Tần suất\n(total_orders)', 'Giá trị TB Đơn\n(avg_order_value)']
    num_vars = len(categories)

    # 3. Tính góc
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1] # Khép kín

    # 4. Vẽ Radar
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    colors = ['#E74C3C', '#27AE60', '#F1C40F', '#34495E']
    
    # Lấy tên cụm tự động từ index của summary_df (nếu có), hoặc dùng mặc định
    labels = [f"Cụm {i}" for i in range(len(summary_df))]

    for i in range(len(df_radar)):
        values = df_radar.iloc[i].tolist()
        values += values[:1]
        
        ax.plot(angles, values, color=colors[i % len(colors)], linewidth=2.5, linestyle='solid', label=labels[i])
        ax.fill(angles, values, color=colors[i % len(colors)], alpha=0.15)

    # 5. Trang trí
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=12, fontweight='bold')
    ax.set_yticklabels([])
    
    plt.title('Hồ sơ Phân khúc Khách hàng RFM (Radar Chart)', size=16, fontweight='bold', y=1.1)
    plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), fontsize=11)
    
    plt.tight_layout()
    
    # Lưu file nếu có đường dẫn
    if save_path:
        save(save_path)
        
    plt.show()