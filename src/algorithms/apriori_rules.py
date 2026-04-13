import pandas as pd
# TODO: import các hàm apriori và association_rules từ thư viện mlxtend
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules

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

        # Khai báo biến sử dụng chuyển đổi ma trận OHE
        ohe = TransactionEncoder()
        """
        Lênh fit dùng để học các sản phẩm phân biệt có trong tập
        Lệnh transform để chuyển đổi các sản phẩm ở lệnh fit thành label của ma trận và xuất dưới dạng thưa sparse = True, nghĩa là chỉ lưu vị trí những giá trị bằng 1
        """
        ohematrix = ohe.fit(self.df_rules['item_list']).transform(self.df_rules['item_list'], sparse=True)

        # Chuyển đổi thành Sparse DataFrame cho panda
        self.df_encoded = pd.DataFrame(ohematrix.toarray(), columns=ohe.columns_)

    def find_frequent_itemsets(self, min_support=0.01):
        """
        Tìm các tập phổ biến (Frequent Itemsets) dựa trên ma trận đã được mã hóa.
        """
        if self.df_encoded is None:
            self.preprocess_data()

        # TODO: gọi hàm apriori() của mlxtend

        self.frequent_itemsets = apriori(self.df_encoded, min_support=min_support, use_colnames=True)
        return self.frequent_itemsets

    def generate_rules(self, metric="confidence", min_threshold=0.2):
        """
        Sinh luật kết hợp từ các tập phổ biến
        """
        if self.frequent_itemsets is None:
            return None

        # TODO: gọi hàm association_rules() của mlxtend

        self.rules = association_rules(self.frequent_itemsets, metric=metric, min_threshold=min_threshold)   
        return self.rules

    def get_top_rules(self, sort_by='lift', top_n=10):
        """
        Lọc và trả về Top các luật tốt nhất (có lift cao nhất > 1)
        """
        # TODO: code sort bảng self.rules theo cột 'sort_by' và lấy top_n dòng đầu tiên.
        if self.rules is None:
            return None
        
        top_rules = (
            self.rules[self.rules['lift'] > 1]
            .sort_values(by=sort_by, ascending=False)
            .head(top_n)
        )
        return top_rules
    
    def count_rules(self):
        """
        Trả về số lượng luật đã sinh ra.
        """
        if self.rules is not None:
            return len(self.rules)
        return 0
    
    def summary(self):
        """In tóm tắt kết quả để debug nhanh."""
        print(f"Số giao dịch       : {len(self.df_rules)}")

        if self.frequent_itemsets is not None:
            print(f"Số tập phổ biến    : {len(self.frequent_itemsets)}")
            size_counts = self.frequent_itemsets['itemsets'].apply(len).value_counts().sort_index()
            for size, count in size_counts.items():
                print(f"  - Tập {size} mục     : {count}")
        
        if self.rules is not None:
            print(f"Số luật sinh được  : {len(self.rules)}")
            print(f"  Confidence (avg) : {self.rules['confidence'].mean():.3f}")
            print(f"  Lift (avg)       : {self.rules['lift'].mean():.3f}")
        else:
            print("Số luật sinh được  : 0")