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
