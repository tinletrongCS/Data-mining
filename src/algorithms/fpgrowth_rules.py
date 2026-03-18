import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import fpgrowth, association_rules
class FPGrowth:
    """
    Class khai phá luật kết hợp sử dụng thuật toán FP-Growth .
    """

    def __init__(self, df_rules: pd.DataFrame):
        self.df_rules = df_rules
        self.df_encoded = None
        self.frequent_itemsets = None
        self.rules = None

    def preprocess_data(self):
        """
        Chuyển đổi cột 'item_list' thành ma trận One-Hot Encoding.
        Nếu đơn hàng có sản phẩm A thì tại cột A sẽ có giá trị 1, ngược lại là 0
        """
        # Khai báo biến sử dụng chuyển đổi ma trận OHE
        ohe = TransactionEncoder()
        """
        Lênh fit dùng để học các sản phẩm phân biệt có trong tập
        Lệnh transform để chuyển đổi các sản phẩm ở lệnh fit thành label của ma trận và xuất dưới dạng thưa sparse = True, nghĩa là chỉ lưu vị trí những giá trị bằng 1
        """
        ohematrix = ohe.fit(self.df_rules['item_list']).transform(self.df_rules['item_list'], sparse=True)
        # Chuyển đổi thành Sparse DataFrame cho panda
        self.df_encoded = pd.DataFrame.sparse.from_spmatrix(ohematrix, columns=ohe.columns_)

    def build_fp_tree_and_mine(self, min_support=0.01):
        # Xây cây FP-Tree và tìm các tập phổ biến (Frequent Itemsets).
        if self.df_encoded is None: self.preprocess_data()
        self.frequent_itemsets = fpgrowth(
            self.df_encoded,
            min_support=min_support, # Ngưỡng tối thiểu để xem là phổ biến
            use_colnames=True # Trả đúng tên sản phẩm, False là sẽ là index
        )

    def generate_rules(self,metric='lift', min_threshold=1.2):
        """
        Sinh luật kết hợp dựa trên FP-Tree
        Dùng lift làm tiêu chuẩn lọc vì confidence cao với một sản phẩm cực phổ biến không có nghĩa là chúng có liên quan với nhau
            Lift = 1: A và B hoàn toàn độc lập
            Lift > 1: A và B tương quan thuận, khách mua A sẽ có xu hướng mua B cao hơn so với người bình thường.
            Lift < 1: A và B tương quan nghịch nhau, Việc mua A làm giảm khả năng mua B.
        """
        if self.frequent_itemsets is None: self.build_fp_tree_and_mine()
        # Nếu tập phổ biến trống (do min_support quá cao) sẽ xuất thông báo
        if self.frequent_itemsets.empty:
            print("Không tìm thấy tập phổ biến nào, cần giảm min_support.")
            self.rules = pd.DataFrame()
            return self.rules
        # Gọi hàm association_rules() của mlxtend để sinh luật kết hợp
        self.rules = association_rules(
            self.frequent_itemsets, # FP-Tree
            metric=metric, # lift
            min_threshold=min_threshold
        )
        return self.rules

    def recommend_products(self, cart_items: list) -> list:
        """
        Hàm gọi ý mua thêm sản phẩm từ giỏ hàng hiện tại
        """
        if self.rules is None or self.rules.empty: return []
        # Chuyển giỏ hàng thành frozenset để so sánh tập hợp, định dạng bắt buộc của mlxtend
        cart_set = frozenset(cart_items)
        # Khởi tạo danh sách recommend dưới dạng tập hợp để thực hiện các phép toán trên chúng
        recommend = set()
        # Lọc các luật mà vế trái (antecedents) là tập con của giỏ hàng
        matched_rules = self.rules[self.rules['antecedents'].apply(lambda x: x.issubset(cart_set))]
        # Sắp xếp các luật theo mức độ ưu tiên (lift cao nhất, sau đó đến confidence)
        matched_rules = matched_rules.sort_values(by=['lift', 'confidence'], ascending=[False, False])
        # Lấy vế phải (consequents) của các luật để làm gợi ý, dùng update để loại bỏ trùng lặp cho tập hợp
        for consequents in matched_rules['consequents']: recommend.update(consequents)
        # Loại bỏ những sản phẩm đã có sẵn trong giỏ hàng, tránh gợi ý lại đồ đã mua
        recommend.difference_update(cart_set)
        return list(recommend)