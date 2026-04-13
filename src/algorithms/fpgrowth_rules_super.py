import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import fpgrowth, association_rules

class FPGrowthSuper:

    def __init__(self, df_rules: pd.DataFrame):
        self.df_rules = df_rules
        self.df_encoded = None
        self.frequent_itemsets = None
        self.rules = None

    def preprocess_data(self):
        """
        Chuyển đổi cột 'item_list' thành ma trận One-Hot Encoding.
        """
        ohe = TransactionEncoder()
        ohematrix = ohe.fit(self.df_rules['item_list']).transform(self.df_rules['item_list'], sparse=True)
        # Chuyển đổi thành Sparse DataFrame cho panda
        self.df_encoded = pd.DataFrame.sparse.from_spmatrix(ohematrix, columns=ohe.columns_)

    def build_fp_tree_and_mine(self, item_supports: dict = None, default_support=0.01):
        if self.df_encoded is None: self.preprocess_data()

        # Nếu không có dict ngưỡng riêng, chạy cơ bản
        if item_supports is None:
            self.frequent_itemsets = fpgrowth(self.df_encoded, min_support=default_support, use_colnames=True)
            return

        # BƯỚC 1: KHAI PHÁ THÔ (Lấy ngưỡng thấp nhất trong hệ thống)
        lowest_support = min(item_supports.values()) if item_supports else default_support
        raw_itemsets = fpgrowth(
            self.df_encoded,
            min_support=lowest_support, 
            use_colnames=True 
        )

        # BƯỚC 2: LỌC CHẶT (Áp dụng Ràng buộc cực đại)
        if raw_itemsets.empty:
            print("Không tìm thấy tập mục nào với ngưỡng thấp nhất.")
            self.frequent_itemsets = raw_itemsets
            return

        def check_max_constraint(row):
            itemset = row['itemsets']
            actual_support = row['support']
            # Tìm ngưỡng yêu cầu lớn nhất trong số các mặt hàng của tập hợp này
            required_support = max([item_supports.get(item, default_support) for item in itemset])
            return actual_support >= required_support

        mask = raw_itemsets.apply(check_max_constraint, axis=1)
        self.frequent_itemsets = raw_itemsets[mask].reset_index(drop=True)

    def generate_rules(self, item_supports: dict = None, default_support=0.01, metric='lift', min_threshold=1.2, min_confidence=0.1):
        """
        Sinh luật kết hợp dựa trên FP-Tree
        """
        if self.frequent_itemsets is None: 
            self.build_fp_tree_and_mine(item_supports, default_support)
            
        if self.frequent_itemsets.empty:
            print("Không tìm thấy tập mục phổ biến nào, cần giảm min_threshold hoặc support.")
            self.rules = pd.DataFrame()
            return self.rules

        # 1. Sinh luật thô dựa trên tiêu chí chính 
        raw_rules = association_rules(
            self.frequent_itemsets, 
            metric=metric, 
            min_threshold=min_threshold
        )
        
        # 2. Lọc chặt bằng Confidence 
        if not raw_rules.empty:
            self.rules = raw_rules[raw_rules['confidence'] >= min_confidence].reset_index(drop=True)
        else:
            self.rules = raw_rules
            
        return self.rules

    def recommend_products(self, cart_items: list) -> list:
        """
        Hàm gợi ý mua thêm sản phẩm từ giỏ hàng hiện tại
        """
        if self.rules is None or self.rules.empty: return []
        cart_set = frozenset(cart_items)
        recommend = set()
        matched_rules = self.rules[self.rules['antecedents'].apply(lambda x: x.issubset(cart_set))]
        matched_rules = matched_rules.sort_values(by=['lift', 'confidence'], ascending=[False, False])
        
        for consequents in matched_rules['consequents']: 
            recommend.update(consequents)
            
        recommend.difference_update(cart_set)
        return list(recommend)