import numpy as np # TÔN ĐANG GÕ NÈ
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix, accuracy_score
from sklearn.model_selection import cross_val_score
path = "jewelry.csv"
column_names = [
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
dataset = pd.read_csv(path, header=None, names=column_names)

print(dataset.shape)
print(dataset.head(5))