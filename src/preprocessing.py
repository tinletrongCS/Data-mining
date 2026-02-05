import pandas as pd
from sklearn.preprocessing import MinMaxScaler, LabelEncoder
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
        df['price'] = pd.to_numeric(df['price'], errors='coerce').fillna(0.0)
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
    - Chuyển về lowercase để đồng nhất (Gold hay gold gì đều như nhau nha).
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
    df = format_id_columns(df)
    df = format_datetime_column(df)
    df = format_price_column(df)
    df = drop_missing_critical_ids(df)
    df = clean_category_column(df)
    df = clean_product_attributes(df)
    
    return df

# =============================================================================
# 2. TRÍCH XUẤT ĐẶC TRƯNG THỜI GIAN
# Mục tiêu: Phục vụ phân tích xu hướng mua sắm
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
    pass

def run_phase_2_cleaning(df: pd.DataFrame) -> pd.DataFrame:
    df = extract_time_features(df)

    return df

# =============================================================================
# 3. BIẾN ĐỔI DỮ LIỆU (TRANSFORMATION)
# Mục tiêu: Tạo ra các dataset con phù hợp cho từng thuật toán (Luật kết hợp, Gom cụm).
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
    """
    pass

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
    pass


def encode_and_scale_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    TODO - Mã hóa biến phân loại và Chuẩn hóa biến số.
    """
    # 1. MÃ HÓA (ENCODING): Chuyển chữ thành số
    # Các cột cần mã hóa
    cat_cols = ['gender', 'color', 'metal', 'gem', 'category_code', 'price_segment']
    existing_cats = [col for col in cat_cols if col in df.columns]

    le = LabelEncoder()
    for col in existing_cats:
        df[f'{col}_encoded'] = le.fit_transform(df[col].astype(str))

    num_cols = ['price', 'quantity']
    if 'hour' in df.columns:
        num_cols.append('hour')

    existing_nums = [col for col in num_cols if col in df.columns]

    scaler = MinMaxScaler()
    for col in existing_nums:
        df[f'{col}_scaled'] = scaler.fit_transform(df[[col]])

    return df

def run_phase_3_cleaning(df: pd.DataFrame) -> pd.DataFrame:
    df = transform_for_association_rules(df)
    df = transform_for_user_profile(df)

    return df

# =============================================================================
# 4. XỬ LÝ NHIỄU & NGOẠI LAI (OUTLIERS)
# Mục tiêu: Loại bỏ các dữ liệu rác làm sai lệch mô hình.
# =============================================================================

def remove_outliers(df: pd.DataFrame) -> pd.DataFrame:
    """
    TODO: Loại bỏ các dòng dữ liệu bất thường.
        Yêu cầu:
        - price <= 0: Xóa.
        - quantity < 0: Xóa (hàng trả lại/lỗi).
        - Xử lý các đơn hàng có giá trị quá lớn bất thường nếu cần.
    """
    pass

def run_phase_4_cleaning(df: pd.DataFrame) -> pd.DataFrame:
    df = remove_outliers(df)

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

    df = remove_outliers(df)

    df = extract_time_features(df)
    df = create_price_segments(df)

    df = encode_and_scale_features(df)

    # Gom nhóm và biến đổi
    df_rules = transform_for_association_rules(df)
    df_users = transform_for_user_profile(df)

    return df ,df_users