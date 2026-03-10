import pandas as pd


class FPGrowth:

    def __init__(self, df_rules: pd.DataFrame):
        # df_rules là bảng có 2 cột: 'order_id' và 'item_list'
        self.df_rules = df_rules
        self.df_encoded = None
        self.frequent_itemsets = None
        self.rules = None

    def preprocess_data(self):
        """
        Chuyển đổi cột 'item_list' thành ma trận One-Hot Encoding.
        - Input: List các items trong mỗi order.
        - Output: DataFrame với các cột là tên sản phẩm, giá trị là True/False hoặc 1/0.
        vd 1 đơn hàng mua như sau: ID = 123 ['earring', 'ring', 'necklace']
        ma trận sẽ là
        ID ... earring ... ... ring ... necklace ...
        123     True           True      True
        những chỗ ... là những loại đá quý khác, và có giá trị là False
        """
        # TODO: chuyển đổi df_rules thành ma trận df_encoded
        pass

    def build_fp_tree_and_mine(self, min_support=0.01):
        """
        Xây cây FP-Tree
        dùng cấu trúc cây để chạy nhanh hơn.
        """
        if self.df_encoded is None:
            self.preprocess_data()

        # TODO: gọi hàm fpgrowth() của mlxtend
        pass

    def generate_rules(self, metric='lift', min_threshold=1.2):
        """
        Sinh luật kết hợp.
        Dùng lift làm tiêu chuẩn lọc gốc thay vì confidence để tìm ra các cặp mua chéo tốt nhất.
        """
        if self.frequent_itemsets is None:
            return None

        # TODO: gọi hàm association_rules()
        pass

    def recommend_products(self, cart_items: list) -> list:
        """
        Hàm ứng dụng thực tế.
        Truyền vào giỏ hàng hiện tại (VD: ['ring', 'diamond']),
        trả về danh sách các món nên gợi ý mua kèm.
        """
        # TODO: dùng bảng self.rules để lookup xem cart_items thuộc vế trái nào,
        # sau đó trả về vế phải tương ứng.
        pass