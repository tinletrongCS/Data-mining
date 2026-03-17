import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

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
    """
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Tạo danh sách màu sắc tương ứng với số cụm
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd'][:df_clustered['cluster'].nunique()]

    for cluster_id in sorted(df_clustered['cluster'].unique()):
        # Lọc dữ liệu của từng cụm
        cluster_data = df_clustered[df_clustered['cluster'] == cluster_id]

        # Để đồ thị không bị lag và không bị biến dạng bởi nhóm VIP (Cụm 1),
        # ta lấy mẫu (sample) và có thể dùng np.log1p để scale lại trục cho dễ nhìn
        ax.scatter(
            cluster_data['recency'],
            cluster_data['total_orders'],
            cluster_data['avg_order_value'],  # Dùng avg_order_value thay vì total_spend để đồ thị bung đều hơn
            label=f'Cluster {cluster_id}',
            alpha=0.6,
            edgecolors='w',
            s=50,
            c=colors[cluster_id % len(colors)]
        )

    ax.set_xlabel('Recency (Ngày)')
    ax.set_ylabel('Total Orders (Số đơn)')
    ax.set_zlabel('Avg Order Value (Giá trị/đơn)')
    ax.set_title('Phân cụm Khách hàng 3D (RFM Space)', fontsize=14, fontweight='bold')

    # Hiển thị chú thích
    ax.legend(title="Clusters", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    if save_path:
        save(save_path)
    plt.show()