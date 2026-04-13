import pandas as pd
import numpy as np
from typing import Tuple
from sklearn.preprocessing import MinMaxScaler
# =============================================================================
# 1. LÀM SẠCH CƠ BẢN VÀ ĐỔI TÊN CỘT
# Chú ý: Khi gọi các hàm ở đây thì truyền tham số kiểu bảng, truyền vào dataset
# =============================================================================

def format_id_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    TODO: Xử lý nhóm cột định danh (IDs) -> chuyển thành string hết
    """
    id_columns = ['order_id', 'product_id', 'category_id', 'brand_id', 'user_id']
    existing_columns = list(filter(lambda col: col in df.columns, id_columns))
    for col in existing_columns:
        df[col] = df[col].fillna('unknown')
        df[col] = df[col].astype(str).str.replace(r'\.0$', '', regex=True)
    return df

def format_datetime_column(df: pd.DataFrame) -> pd.DataFrame:
    """
    TODO: Chuyển đổi event_time sang kiểu dữ liệu datetime
    """
    if 'event_time' in df.columns:
        df['event_time'] = pd.to_datetime(df['event_time'], errors='coerce')
    return df

def format_price_column(df: pd.DataFrame) -> pd.DataFrame:
    """
    TODO: Xử lý cột giá (price) -> float
    """
    if 'price' in df.columns:
        df['price'] = pd.to_numeric(df['price'], errors='coerce')
        # những hàng nào không chứa giá trị cột price thì bỏ luôn
        # do dùng trong k means thì những giá trị 0 này sẽ gây lệch
        df = df.dropna(subset=['price']).copy()
    return df

def drop_missing_critical_ids(df: pd.DataFrame) -> pd.DataFrame:
    """
    TODO: Kiểm tra user_id và product_id -> Thiếu cả 2 thì bỏ
    """
    critical_cols = ['user_id', 'product_id']
    target_cols = [col for col in critical_cols if col in df.columns]
    if target_cols:
        mask = (df[target_cols] == 'unknown').any(axis=1)
        df = df[~mask].copy()
    return df

def clean_category_column(df: pd.DataFrame) -> pd.DataFrame:
    """
    TODO: Xử lý chuỗi: Loại bỏ tiền tố 'jewelry.' (VD: 'jewelry.ring' -> 'ring').
    """
    if 'category_code' in df.columns:
        df['category_code'] = df['category_code'].fillna('unknown').astype(str)
        df['category_code'] = df['category_code'].apply(lambda x: x.split('.')[-1] if '.' in x else x)
    return df

def clean_product_attributes(df: pd.DataFrame) -> pd.DataFrame:
    """
    TODO: Columns: gender, color, metal, gem
        Chuyển về lowercase để đồng nhất (Gold hay gold gì đều như nhau nha).
    """
    cols = ['gender', 'color', 'metal', 'gem']
    for col in cols:
        if col in df.columns:
            df[col] = df[col].fillna('unknown').astype(str).str.lower()
    return df

def run_phase_1_cleaning(df: pd.DataFrame) -> pd.DataFrame:
    """
    TODO: Hàm tổng hợp gọi lần lượt các bước làm sạch cơ bản theo thứ tự.
    """
    df.columns = df.columns.str.strip()
    df.columns = df.columns.str.lower()
    df = df.drop_duplicates().copy()

    df = format_id_columns(df)
    df = format_datetime_column(df)
    df = format_price_column(df)
    df = drop_missing_critical_ids(df)
    df = clean_category_column(df)
    df = clean_product_attributes(df)
    
    return df

# =============================================================================
# TODO 2. TRÍCH XUẤT ĐẶC TRƯNG THỜI GIAN
#   Mục tiêu: Phục vụ phân tích xu hướng mua sắm
# =============================================================================

def extract_time_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    TODO: Tạo các cột đặc trưng mới từ cột 'event_time'.
        Output mong đợi gồm các cột:
        - hour: Giờ trong ngày (0-23).
        - weekday: Thứ trong tuần.
        - day: Ngày trong tháng.
        - month: Tháng.
        - is_weekend: 1 nếu là cuối tuần (T7 + CN), 0 nếu ngày thường (T2-T6).
    """
    # BƯỚC QUAN TRỌNG: Ép kiểu lại lần nữa để chắc chắn nó là datetime
    # Nếu nó đã là datetime rồi thì lệnh này chạy rất nhanh, không sao cả.
    if not pd.api.types.is_datetime64_any_dtype(df['event_time']):
        df['event_time'] = pd.to_datetime(df['event_time'], errors='coerce')

    df['hour'] = df['event_time'].dt.hour
    df['day'] = df['event_time'].dt.day
    df['month'] = df['event_time'].dt.month
    # day_of_week trả về số: 0 (Thứ 2) -> 6 (Chủ nhật)
    df['day_of_week'] = df['event_time'].dt.dayofweek

    # hiện tên thứ (Monday, Tuesday...) để vẽ biểu đồ cho đẹp
    df['weekday_name'] = df['event_time'].dt.day_name()
    df['is_weekend'] = df['day_of_week'].apply(lambda x: 1 if x >= 5 else 0)

    return df

def run_phase_2_cleaning(df: pd.DataFrame) -> pd.DataFrame:
    df = extract_time_features(df)

    return df

# =============================================================================
# TODO 3. BIẾN ĐỔI DỮ LIỆU (TRANSFORMATION)
#   Mục tiêu: Tạo ra các dataset con phù hợp cho từng thuật toán (Luật kết hợp, Gom cụm).
# =============================================================================
def create_price_segments(df: pd.DataFrame) -> pd.DataFrame:
    """
    TODO - Tạo phân khúc giá
        Low: < 100 USD
        Mid: 100 USD- 500 USD
        High: > 500 USD
    """
    if 'price' not in df.columns:
        return df

    # Định nghĩa khoảng chia
    bins = [-1, 100, 500, float('inf')]
    labels = ['Low', 'Mid', 'High']

    # Tạo cột mới
    df['price_segment'] = pd.cut(df['price'], bins=bins, labels=labels)

    # Chuyển về string để tránh lỗi category khi lưu file
    df['price_segment'] = df['price_segment'].astype(str)

    return df

def transform_for_association_rules(df: pd.DataFrame) -> pd.DataFrame:
    """
    TODO: Chuẩn bị dữ liệu cho bài toán Khai phá luật kết hợp (Association Rules).
        Yêu cầu:
        - Lọc các đơn hàng có quantity > 0.
        - Gom nhóm theo 'order_id'.
        - Output: Một DataFrame mà mỗi dòng là một đơn hàng, chứa list các sản phẩm (product_id hoặc category_code).
        VD: Order_1 -> ['Ring', 'Earring']
        earring: Bông tai.
        pendant: Mặt dây chuyền.
        necklace: Vòng cổ / Dây chuyền.
        ring: Nhẫn.
        bracelet: Vòng tay / Lắc tay.
        brooch: Ghim cài áo
        unknown: Các sản phẩm chưa được phân loại rõ ràng trong hệ thống.
    """
    # Lọc các đơn hàng hợp lệ (quantity > 0) và category_code khác 'unknown'
    df_rules = df[(df['quantity'] > 0) & (df['category_code'] != 'unknown')].copy()
    # Gom nhóm theo order_id
    df_rules = df_rules.groupby('order_id')['category_code'].apply(lambda x: list(set(x))).reset_index()#  Bỏ reset_index() sẽ bị lỗi khi chạy apriori vì không còn là DataFrame nữa.
    # Đổi tên cột cho dễ hiểu
    df_rules.rename(columns={'category_code': 'item_list'}, inplace=True) # Không có inplace=True sẽ không đổi tên cột được
    return df_rules

# Hàm này quan trọng
def transform_for_user_profile(df: pd.DataFrame) -> pd.DataFrame:
    """
    TODO: Chuẩn bị dữ liệu cho bài toán Gom cụm khách hàng (Clustering) & Phân loại.
        Yêu cầu:
        - Gom nhóm theo 'user_id'.
        - Tính toán các chỉ số tổng hợp (RFM + Preferences):
            + total_spend (Sum price)
            + total_orders (Count unique order_id)
            + avg_order_value
            + recency (Số ngày từ lần mua cuối)
            + favorite_gem (Mode gem)
    """
    valid_df = df[
        (df['user_id'].notna()) &
        (df['order_id'].notna()) &
        (df['price'] > 0)
        ].copy()
    if valid_df.empty:
        return pd.DataFrame()  

    last_time_in_data = valid_df['event_time'].max()

    def favorite_gem_list(x):
        counts = x.value_counts()
        if counts.empty: return ['unknown']
        max_count = counts.max()
        return counts[counts == max_count].index.tolist()

    agg_rules = {
        'price': 'sum',
        'order_id': 'nunique',
        'event_time': 'max',
        'gem': favorite_gem_list
    }
    df_users = valid_df.groupby('user_id').agg(agg_rules).reset_index()

    df_users.rename(columns={
        'price': 'total_spend',
        'order_id': 'total_orders',
        'event_time': 'last_purchase_date',
        'gem': 'favorite_gems'
    }, inplace=True)
    # Recency: Ngày cuối file - Ngày cuối của user
    df_users['recency'] = (last_time_in_data - df_users['last_purchase_date']).dt.days

    # Tổng chi
    df_users['avg_order_value'] = (df_users['total_spend'] / df_users['total_orders']).round(2)  
    
    # Tổng đơn
    df_users['total_spend'] = df_users['total_spend'].round(2)

    # Xử lý an toàn cho Recency
    df_users['recency'] = df_users['recency'].clip(lower=0)  # Đảm bảo không có giá trị âm do lệch thời gian

    df_users = df_users.drop(columns=['last_purchase_date'])
    return df_users

def encode_and_scale_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    TODO - Mã hóa biến phân loại
    """
    cat_cols = ['gender', 'color', 'metal', 'gem', 'category_code', 'price_segment']
    existing_cats = [col for col in cat_cols if col in df.columns]
    # drop_first để loại bỏ đa cộng tuyến
    df = pd.get_dummies(df, columns=existing_cats, drop_first=False, dtype=int)
    num_cols = ['price', 'quantity']
    if 'hour' in df.columns:
        num_cols.append('hour')

    existing_nums = [col for col in num_cols if col in df.columns]
    scaler = MinMaxScaler()
    #  fit 1 lần cho toàn bộ feature 
    df[[f"{col}_scaled" for col in existing_nums]] = scaler.fit_transform(df[existing_nums])
    return df

def run_phase_3_cleaning(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    df_rules = transform_for_association_rules(df.copy())
    df_users = transform_for_user_profile(df.copy())

    return df_rules, df_users

# =============================================================================
# TODO - 4. XỬ LÝ NHIỄU & NGOẠI LAI (OUTLIERS)
#   Mục tiêu: Loại bỏ các dữ liệu rác làm sai lệch mô hình.
# =============================================================================

def remove_outliers(df: pd.DataFrame) -> pd.DataFrame:
    """
    TODO: Loại bỏ các dòng dữ liệu bất thường.
        Yêu cầu:
        - price <= 0: Xóa.
        - quantity < 0: Xóa
        - Xử lý các đơn hàng có giá trị lớn bất thường.
    """
    df = df[(df['price'] >= 0) & (df['quantity'] > 0)].copy()

    upper_limit = df['price'].quantile(0.999)
    df_clean = df[df['price'] <= upper_limit].copy()

    return df_clean

def run_phase_4_cleaning(df: pd.DataFrame) -> pd.DataFrame:
    df = remove_outliers(df)

    return df


# =============================================================================
# ! TODO - 5. PHÂN TÍCH TƯƠNG QUAN (CORRELATION ANALYSIS)
# =============================================================================
def handle_correlated_features(df: pd.DataFrame, feature_cols: list, threshold: float = 0.8) -> pd.DataFrame:
    df_check = df[feature_cols].copy()

    # Tính ma trận tương quan Pearson
    corr_matrix = df_check.corr(method='pearson').abs()

    # Lấy nửa trên của ma trận để tránh lấy đường chéo
    upper_tri = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))

    # Tìm các cột có độ tương quan > threshold và đánh dấu để loại bỏ
    to_drop = [column for column in upper_tri.columns if any(upper_tri[column] > threshold)]

    if to_drop:  
        df = df.drop(columns=to_drop)
    return df
# =============================================================================
# PIPELINE
# =============================================================================

def master_preprocessing_pipeline(df):
    """
    TODO: Hàm chạy toàn bộ quy trình tiền xử lý.
        Returns:
            Một dictionary chứa các DataFrame đã xử lý sẵn sàng cho từng bài toán:
            {
                "main_clean": df_clean,
                "rules_data": df_rules,
                "user_profile": df_users
            }
    """
    df = run_phase_1_cleaning(df)
    df = run_phase_4_cleaning(df)
    df = run_phase_2_cleaning(df)
    df = create_price_segments(df)

    df_rules, df_users = run_phase_3_cleaning(df)

    # ! Lọc biến dư thừa cho tập RFM trước khi trả về cho K-Means ->  loại bỏ đa cộng tuyến 
    rfm_cols = ['recency', 'total_orders', 'total_spend', 'avg_order_value']
    df_users = handle_correlated_features(df_users, rfm_cols, threshold=0.8)

    df_main_clean = encode_and_scale_features(df.copy())
    return {
        "main_clean": df_main_clean,
        "rules_data": df_rules,
        "user_profile": df_users
    }
