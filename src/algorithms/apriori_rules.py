import pandas as pd
# TODO: import các hàm apriori và association_rules từ thư viện mlxtend

class Apriori:

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
        """
        # TODO: chuyển đổi df_rules thành ma trận df_encoded
        # Dùng TransactionEncoder của mlxtend

        # self.df_encoded = ...
        pass

    def find_frequent_itemsets(self, min_support=0.01):
        """
        Tìm các tập phổ biến bằng
        """
        if self.df_encoded is None:
            self.preprocess_data()

        # TODO: gọi hàm apriori() của mlxtend

        # self.frequent_itemsets = ...
        pass

    def generate_rules(self, min_confidence=0.2):
        """
        Sinh luật kết hợp từ các tập phổ biến
        """
        if self.frequent_itemsets is None:
            return None

        # TODO: gọi hàm association_rules() của mlxtend

        # self.rules = ...
        # return self.rules
        pass

    def get_top_rules(self, sort_by='lift', top_n=10):
        """
        Lọc và trả về Top các luật tốt nhất (có confidence cao nhất > 1)
        """
        # TODO: code sort bảng self.rules theo cột 'sort_by' và lấy top_n dòng đầu tiên.
        pass