# Test gọi hàm
def func_1():
    print("From src/visualization.py:", 'xin chao')

import pandas as pd

# =============================================================================
# 1. LÀM SẠCH CƠ BẢN 
# Chú ý: Khi gọi các hàm ở đây thì truyền tham số kiểu bảng, truyền vào dataset 
# =============================================================================

def format_id_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Xử lý nhóm cột định danh (IDs).
    
    Nhiệm vụ:
    - Chuyển đổi order_id, product_id, category_id, branch_id, user_id sang string
    - Đảm bảo các ID lớn không bị lỗi hiển thị (e+18).
    """
    pass

def format_datetime_column(df: pd.DataFrame) -> pd.DataFrame:
    """
    - Chuyển đổi event_time sang kiểu dữ liệu datetime 
    - Xử lý lỗi nếu định dạng thời gian không hợp lệ 
    """
    pass

def format_price_column(df: pd.DataFrame) -> pd.DataFrame:
    """
    Xử lý cột giá (price).
    
    Nhiệm vụ:
    - Ép kiểu sang float.
    - Có thể xử lý nhanh các giá trị price < 0 
    """
    pass

def drop_missing_critical_ids(df: pd.DataFrame) -> pd.DataFrame:
    """
    Xử lý dòng thiếu dữ liệu quan trọng.
    
    Nhiệm vụ:
    - Kiểm tra user_id và product_id.
    - Nếu dòng nào thiếu 1 trong 2 trường này -> Xóa dòng.
    - Lý do: Không thể định danh giao dịch nếu thiếu người mua hoặc vật được mua.
    """
    pass

def clean_category_column(df: pd.DataFrame) -> pd.DataFrame:
    """
    Làm sạch đặc thù cột category_code.
    
    Nhiệm vụ:
    - Điền khuyết (fillna) bằng 'unknown'.
    - Xử lý chuỗi: Loại bỏ tiền tố 'jewelry.' (VD: 'jewelry.ring' -> 'ring').
    - Ép kiểu sang string.
    """
    pass

def clean_product_attributes(df: pd.DataFrame) -> pd.DataFrame:
    """
    Làm sạch nhóm thuộc tính sản phẩm (Metadata).
    
    Columns: gender, color, metal, gem
    Nhiệm vụ:
    - Điền khuyết (fillna) bằng 'unknown'.
    - Chuyển về lowercase để đồng nhất (Gold hay gold gì đều như nhau nha).
    - Ép kiểu sang string.
    """
    pass

def run_phase_1_cleaning(df: pd.DataFrame) -> pd.DataFrame:
    """
    Hàm tổng hợp gọi lần lượt các bước làm sạch cơ bản theo thứ tự.
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
    Tạo các cột đặc trưng mới từ cột 'event_time'.
    
    Output mong đợi gồm các cột:
    - hour: Giờ trong ngày (0-23).
    - weekday: Thứ trong tuần.
    - day: Ngày trong tháng.
    - month: Tháng.
    - is_weekend: 1 nếu là cuối tuần (T7 + CN), 0 nếu ngày thường (T2-T6).
    """
    pass

# =============================================================================
# 3. BIẾN ĐỔI DỮ LIỆU (TRANSFORMATION)
# Mục tiêu: Tạo ra các dataset con phù hợp cho từng thuật toán (Luật kết hợp, Gom cụm).
# =============================================================================

def transform_for_association_rules(df: pd.DataFrame) -> pd.DataFrame:
    """
    Chuẩn bị dữ liệu cho bài toán Khai phá luật kết hợp (Association Rules).
    
    Yêu cầu:
    - Lọc các đơn hàng có quantity > 0.
    - Gom nhóm theo 'order_id'.
    - Output: Một DataFrame mà mỗi dòng là một đơn hàng, chứa list các sản phẩm (product_id hoặc category_code).
      VD: Order_1 -> ['Ring', 'Earring']
    """
    pass

def transform_for_user_profile(df: pd.DataFrame) -> pd.DataFrame:
    """
    Chuẩn bị dữ liệu cho bài toán Gom cụm khách hàng (Clustering) & Phân loại.
    
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

# =============================================================================
# 4. XỬ LÝ NHIỄU & NGOẠI LAI (OUTLIERS)
# Mục tiêu: Loại bỏ các dữ liệu rác làm sai lệch mô hình.
# =============================================================================

def remove_outliers(df: pd.DataFrame) -> pd.DataFrame:
    """
    Loại bỏ các dòng dữ liệu bất thường.
    
    Yêu cầu:
    - price <= 0: Xóa.
    - quantity < 0: Xóa (hàng trả lại/lỗi).
    - Xử lý các đơn hàng có giá trị quá lớn bất thường nếu cần.
    """
    pass

# =============================================================================
# PIPELINE
# =============================================================================

def master_preprocessing_pipeline(filepath: str) -> dict:
    """
    Hàm chạy toàn bộ quy trình tiền xử lý từ A-Z.
    
    Returns:
        Một dictionary chứa các DataFrame đã xử lý sẵn sàng cho từng bài toán:
        {
            "main_clean": df_clean,
            "rules_data": df_rules,
            "user_profile": df_users
        }
    """
    # 1. Load Data
    # 2. Basic Cleaning (Phase 1)
    # 3. Outlier Removal (Phase 4 - nên làm sớm để sạch data)
    # 4. Feature Extraction (Phase 2)
    # 5. Transformation (Phase 3)
    pass