from reports.models import (
    CashFlowItem,
    CashFlowRecord,
    BusinessActivity,
)

OPERATING_ACTIVITY = BusinessActivity.objects.get(name="Operating Activity")
INVESTING_ACTIVITY = BusinessActivity.objects.get(name="Investing Activity")
FINANCING_ACTIVITY = BusinessActivity.objects.get(name="Financing Activity")


def choose_activity(activity: str):
    if activity == OPERATING_ACTIVITY.name:
        return OPERATING_ACTIVITY

    elif activity == INVESTING_ACTIVITY.name:
        return INVESTING_ACTIVITY

    elif activity == FINANCING_ACTIVITY.name:
        return FINANCING_ACTIVITY


class GenerateCFReport:
    def __init__(self, transactions) -> None:
        self.transactions = transactions

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

    def group_transactions(self):
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

        return {
            "Operating Inflow": self.operating_activities_inflow,
            "Operating Outflow": self.operating_activities_outflow,
            "Investing Inflow": self.investing_activities_inflow,
            "Investing Outflow": self.investing_activities_outflow,
            "Financing Inflow": self.financing_activities_inflow,
            "Financing Outflow": self.financing_activities_outflow,
        }

    @classmethod
    def reduce_data(cls, transactions):
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

    @classmethod
    def create_records(cls, statement_uid, data):
        for item in data:
            category = item["category"]
            subcategory = item["subcategory"]

            report_item = CashFlowItem.objects.create(
                name=f"{category}-{subcategory}",
                is_income=True if item["type"] == "receivable" else False,
                activity=choose_activity(item["activity"]),
            )

            CashFlowRecord.objects.create(
                statement_uid=statement_uid,
                amount=item["amount"],
                item=report_item,
            )

        return
