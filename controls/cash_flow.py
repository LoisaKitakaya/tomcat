from reports.models import CashFlowRecord
from transactions.models import BusinessActivity


def choose_activity(activity: str):
    """
    Choose a business activity.
    """

    try:
        OPERATING_ACTIVITY = BusinessActivity.objects.get(name="Operating Activity")
        INVESTING_ACTIVITY = BusinessActivity.objects.get(name="Investing Activity")
        FINANCING_ACTIVITY = BusinessActivity.objects.get(name="Financing Activity")

    except:
        OPERATING_ACTIVITY = BusinessActivity.objects.create(name="Operating Activity")
        INVESTING_ACTIVITY = BusinessActivity.objects.create(name="Investing Activity")
        FINANCING_ACTIVITY = BusinessActivity.objects.create(name="Financing Activity")

    if activity == OPERATING_ACTIVITY.name:
        return OPERATING_ACTIVITY

    elif activity == INVESTING_ACTIVITY.name:
        return INVESTING_ACTIVITY

    elif activity == FINANCING_ACTIVITY.name:
        return FINANCING_ACTIVITY


class GenerateCFReport:
    """
    Generates a Cash Flow report (CFS).

    NOTE: This class is strictly meant to be used to generate only Cash Flow reports.
    """

    def __init__(self, transactions: list) -> None:
        self.transactions = transactions

        self.record_uid = ""

        self.ACTIVITIES = (
            {
                "Operating Activity": (
                    "Revenue Transactions",
                    "Expense Transactions",
                )
            },
            {
                "Investing Activity": (
                    "Asset Transactions",
                    "Financial Transactions",
                )
            },
            {
                "Financing Activity": (
                    "Liability Transactions",
                    "Equity Transactions",
                )
            },
        )

        self.operating_activities_inflow = []
        self.operating_activities_outflow = []

        self.investing_activities_inflow = []
        self.investing_activities_outflow = []

        self.financing_activities_inflow = []
        self.financing_activities_outflow = []

    @property
    def cashflow_uid(self):
        """
        Returns the uid (unique identifier).

        NOTE: This uid will be used to identify the cashflow records.
        """

        return self.record_uid

    @cashflow_uid.setter
    def cashflow_uid(self, uid: str):
        """
        Setter method to change the uid (unique identifier).
        """

        self.record_uid = uid

    def group_transactions(self) -> list:
        """
        Group a list of transactions in order to generate a cashflow statement.
        """

        for transaction in self.transactions:
            if (
                transaction.category.parent.group_name
                == self.ACTIVITIES[0]["Operating Activity"][0]
                or transaction.category.parent.group_name
                == self.ACTIVITIES[0]["Operating Activity"][1]
            ):
                if transaction.transaction_type.type_name == "receivable":
                    self.operating_activities_inflow.append(
                        {
                            "type": "receivable",
                            "activity": "Operating Activity",
                            "amount": transaction.transaction_amount,
                            "category": transaction.category.category_name,
                            "subcategory": transaction.sub_category.category_name,
                        }
                    )
                elif transaction.transaction_type.type_name == "payable":
                    self.operating_activities_outflow.append(
                        {
                            "type": "payable",
                            "activity": "Operating Activity",
                            "amount": transaction.transaction_amount,
                            "category": transaction.category.category_name,
                            "subcategory": transaction.sub_category.category_name,
                        }
                    )

            elif (
                transaction.category.parent.group_name
                == self.ACTIVITIES[1]["Investing Activity"][0]
                or transaction.category.parent.group_name
                == self.ACTIVITIES[1]["Investing Activity"][1]
            ):
                if transaction.transaction_type.type_name == "receivable":
                    self.investing_activities_inflow.append(
                        {
                            "type": "receivable",
                            "activity": "Investing Activity",
                            "amount": transaction.transaction_amount,
                            "category": transaction.category.category_name,
                            "subcategory": transaction.sub_category.category_name,
                        }
                    )
                elif transaction.transaction_type.type_name == "payable":
                    self.investing_activities_outflow.append(
                        {
                            "type": "payable",
                            "activity": "Investing Activity",
                            "amount": transaction.transaction_amount,
                            "category": transaction.category.category_name,
                            "subcategory": transaction.sub_category.category_name,
                        }
                    )

            elif (
                transaction.category.parent.group_name
                == self.ACTIVITIES[2]["Financing Activity"][0]
                or transaction.category.parent.group_name
                == self.ACTIVITIES[2]["Financing Activity"][1]
            ):
                if transaction.transaction_type.type_name == "receivable":
                    self.financing_activities_inflow.append(
                        {
                            "type": "receivable",
                            "activity": "Financing Activity",
                            "amount": transaction.transaction_amount,
                            "category": transaction.category.category_name,
                            "subcategory": transaction.sub_category.category_name,
                        }
                    )
                elif transaction.transaction_type.type_name == "payable":
                    self.financing_activities_outflow.append(
                        {
                            "type": "payable",
                            "activity": "Financing Activity",
                            "amount": transaction.transaction_amount,
                            "category": transaction.category.category_name,
                            "subcategory": transaction.sub_category.category_name,
                        }
                    )

        return [
            self.operating_activities_inflow,
            self.operating_activities_outflow,
            self.investing_activities_inflow,
            self.investing_activities_outflow,
            self.financing_activities_inflow,
            self.financing_activities_outflow,
        ]

    def reduce_data(self, transactions: list) -> list:
        """
        Reduce a list of records such that each record is unique.

        NOTE: The list provided to this method should preferably be a grouping of transactions | consider method: group_transactions().
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

    def create_records(self, data: list) -> None:
        """
        Save a list of records to the database.

        Implementing model CashFlowRecord().

        NOTE: The list provided to this method should preferably be reduced first | consider method: reduce_data().
        """

        for item in data:
            category = item["category"]
            subcategory = item["subcategory"]

            CashFlowRecord.objects.create(
                uid=self.record_uid,
                category=category,
                item=subcategory,
                activity=choose_activity(item["activity"]),
                amount=item["amount"],
                is_income=True if item["type"] == "receivable" else False,
            )

        return
