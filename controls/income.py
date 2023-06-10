class GenerateIncomeReport:
    """
    Generates an Income report (IS).

    NOTE: This class is strictly meant to be used to generate only Income reports.
    """

    def __init__(self, transactions: list) -> None:
        self.transactions = transactions

        self.products = []

        self.record_uid = ""

        self.revenue_list = []
        self.operating_expense_list = []
        self.product_revenue_list = []

    @property
    def inventory_products(self):
        """
        Returns the list of products available to the class.

        NOTE: This product list will be used to calculate the total product profit.
        """

        return self.products

    @inventory_products.setter
    def inventory_products(self, products: list):
        """
        Setter method to change the product list.
        """

        self.products = products

    @property
    def income_uid(self):
        """
        Returns the uid (unique identifier).

        NOTE: This uid will be used to identify the income records.
        """

        return self.record_uid

    @income_uid.setter
    def income_uid(self, uid: str):
        """
        Setter method to change the uid (unique identifier).
        """

        self.record_uid = uid

    def group_data(self) -> dict:
        """
        Group a list of transactions and inventory products in order to generate an income statement.
        """

        for transaction in self.transactions:
            if transaction.transaction_type.type_name == "receivable":
                self.revenue_list.append(
                    {
                        "type": "receivable",
                        "activity": "income",
                        "amount": transaction.transaction_amount,
                        "category": transaction.category.category_name,
                        "subcategory": transaction.sub_category.category_name,
                    }
                )

            elif transaction.transaction_type.type_name == "payable":
                self.operating_expense_list.append(
                    {
                        "type": "payable",
                        "activity": "expense",
                        "amount": transaction.transaction_amount,
                        "category": transaction.category.category_name,
                        "subcategory": transaction.sub_category.category_name,
                    }
                )

        if self.products:
            for product in self.products:
                self.product_revenue_list.append(
                    {
                        "name": product.name,
                        "profit": product.profit_generated,
                        "category": product.category.category_name,
                        "subcategory": product.sub_category.category_name,
                    }
                )

        return {
            "transaction_revenue": self.revenue_list,
            "operating_expense": self.operating_expense_list,
            "product_revenue": self.product_revenue_list,
        }

    def reduce_transaction_data(self, transactions: list) -> list:
        """
        Reduce a list of records such that each record is unique.

        NOTE: The list provided to this method should preferably be a grouping of transactions | consider method: group_data().
        """

        grouped_transactions = {}

        for transaction in transactions:
            activity = transaction["activity"]
            category = transaction["category"]
            subcategory = transaction["subcategory"]
            amount = transaction["amount"]
            transaction_type = transaction["type"]

            key = f"{transaction_type}-{activity}-{category}-{subcategory}"

            if key not in grouped_transactions:
                grouped_transactions[key] = {
                    "type": transaction_type,
                    "activity": activity,
                    "category": category,
                    "subcategory": subcategory,
                    "amount": amount,
                }

            else:
                grouped_transactions[key]["amount"] += amount

        result = list(grouped_transactions.values())

        return result

    def get_total_revenue(self, transactions: list) -> float:
        """
        Get the total revenue by summing up all transactions of type: "receivable".

        NOTE: Best use this method by providing a reduced version of the transactions of type "receivable" | consider method: reduce_transaction_data().
        """

        total_revenue = 0.0

        for transaction in transactions:
            total_revenue += transaction["amount"]

        return total_revenue

    def get_total_product_profit(self, products: list) -> float:
        """
        Get the total product profit by summing up all product profits.
        """

        total_product_profit = 0.0

        for product in products:
            total_product_profit += product["profit"]

        return total_product_profit

    def get_gross_profit(
        self, total_revenue: float, total_product_profit: float
    ) -> float:
        """
        Get the total revenue by summing up the total revenue with the total product profit.

        NOTE: Consider methods: get_total_revenue() and get_total_product_profit().
        """

        return total_revenue + total_product_profit

    def get_total_operation_expense(self, transactions: list) -> float:
        """
        Get the total expenses by summing up all transactions of type: "payable".

        NOTE: Best use this method by providing a reduced version of the transactions of type "payable" | consider method: reduce_transaction_data().
        """

        total_operation_expense = 0.0

        for transaction in transactions:
            total_operation_expense += transaction["amount"]

        return total_operation_expense

    def get_net_income(
        self, gross_profit: float, total_operation_expense: float
    ) -> float:
        """
        Get the net income by subtracting the total operation expanse from the gross profit.

        NOTE: Consider methods: get_gross_profit() and get_total_operation_expense().
        """

        return gross_profit + total_operation_expense
