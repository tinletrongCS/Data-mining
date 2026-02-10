import pandas as pd
import os
from src.preprocessing import master_preprocessing_pipeline

RAW_DATA_PATH = 'data\\raw\\jewelry.csv'
PROCESSED_DIR = 'data\\processed'

COLUMNS_NAME = [
    'event_time',    # Thời gian mua hàng
    'order_id',      # Mã đơn hàng
    'product_id',    # Mã sản phẩm
    'quantity',      # Số lượng
    'category_id',   # Mã danh mục
    'category_code', # Tên loại trang sức
    'brand_id',      # Mã thương hiệu
    'price',         # Giá tiền
    'user_id',       # Mã khách hàng
    'gender',        # Giới tính
    'color',         # Màu sắc (red, white, gold...)
    'metal',         # Chất liệu kim loại (gold, silver...)
    'gem'            # Loại đá quý (diamond, sapphire...)
]

# Ép về string
# tránh để string dài quá đọc csv sẽ tự chuyển sang int64
DTYPE_SPECS = {
    'order_id': str,
    'product_id': str,
    'category_id': str,
    'brand_id': str,
    'user_id': str,
    'category_code': str
}
os.makedirs(PROCESSED_DIR, exist_ok=True)

def read_raw_data(path=RAW_DATA_PATH):
    if not os.path.exists(path):
        print(f"LỖI: Không tìm thấy file tại {path}")
        return None

    try:
        df = pd.read_csv(path, header=None, names=COLUMNS_NAME, dtype=DTYPE_SPECS)
        return df

    except Exception as e:
        print(f"Lỗi khi đọc file CSV: {e}")
        return None

def main():
    df_raw = read_raw_data()

    if df_raw is None:
        return

    data_outputs = master_preprocessing_pipeline(df_raw)

    # main_clean
    main_path = os.path.join(PROCESSED_DIR, 'main_clean.pkl')
    data_outputs['main_clean'].to_pickle(main_path)

    # rules_data
    rules_path = os.path.join(PROCESSED_DIR, 'rules_data.pkl')
    data_outputs['rules_data'].to_pickle(rules_path)

    # user_profile
    user_path = os.path.join(PROCESSED_DIR, 'user_profile.pkl')
    data_outputs['user_profile'].to_pickle(user_path)

if __name__ == "__main__":
    main()
