import json
import random
from plans.models import Plan
from django.test import TestCase, Client
from controls.test_ref import explain_status_code
from transactions.models import (
    TransactionType,
    BusinessActivity,
    TransactionGroup,
    TransactionCategory,
    TransactionSubCategory,
)

from controls.mutation_ref import (
    token_auth,
    create_user,
    create_account,
    create_transaction,
    delete_income_report,
    generate_income_report,
    delete_cash_flow_report,
    generate_cash_flow_report,
    delete_balance_sheet_report,
    generate_balance_sheet_report,
)
from controls.query_ref import (
    get_income_statement,
    get_cash_flow_statement,
    get_all_income_statements,
    get_balance_sheet_statement,
    get_all_cash_flow_statements,
    get_all_balance_sheet_statements,
)


class TestAppMutations(TestCase):
    def setUp(self) -> None:
        self.client = Client()

        self.plan = Plan.objects.create(name="Free")

        create_user_variables = {
            "email": "example@gmail.com",
            "first_name": "Test",
            "last_name": "User",
            "password": "#TestUser15",
            "password2": "#TestUser15",
        }

        response = self.client.post(
            "/graphql/",
            json.dumps(
                {
                    "query": create_user,
                    "variables": create_user_variables,
                }
            ),
            content_type="application/json",
        )

        self.test_username = response.json()["data"]["createUser"]["username"]

        token_auth_variables = {
            "username": self.test_username,
            "password": "#TestUser15",
        }

        get_token = self.client.post(
            "/graphql/",
            json.dumps({"query": token_auth, "variables": token_auth_variables}),
            content_type="application/json",
        )

        self.token = get_token.json()["data"]["tokenAuth"]["token"]

        self.business_activity = BusinessActivity.objects.create(
            name="Operating Activity"
        )

        self.transaction_group = TransactionGroup.objects.create(
            activity=self.business_activity, group_name="Revenue Transactions"
        )

        self.transaction_category = TransactionCategory.objects.create(
            parent=self.transaction_group,
            category_name="Sales",
            category_description="Sales category",
        )
        self.transaction_subcategory = TransactionSubCategory.objects.create(
            parent=self.transaction_category,
            category_name="Product sales",
            category_description="Sales subcategory",
        )

        self.transaction_type_payable = TransactionType.objects.create(
            type_name="payable",
            type_description="Payable description",
        )
        self.transaction_type_receivable = TransactionType.objects.create(
            type_name="receivable",
            type_description="Receivable description",
        )

        variables = {
            "account_name": "KCB test account",
            "account_type": "Savings",
            "account_balance": "20000.00",
            "currency_code": "USD",
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": create_account, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        self.account_id = data["data"]["createAccount"]["id"]

        for i in range(6):
            random_number = random.randint(1, 100)

            if random_number % 2 == 0:
                variables = {
                    "account_id": self.account_id,
                    "transaction_type": self.transaction_type_receivable.type_name,
                    "transaction_amount": "2500.00",
                    "transaction_date": "2023-04-22T13:30",
                    "description": "Test transaction receivable",
                    "category": self.transaction_category.category_name,
                    "sub_category": self.transaction_subcategory.category_name,
                }

            else:
                variables = {
                    "account_id": self.account_id,
                    "transaction_type": self.transaction_type_payable.type_name,
                    "transaction_amount": "1500.00",
                    "transaction_date": "2023-04-20T15:30",
                    "description": "Test transaction payable",
                    "category": self.transaction_category.category_name,
                    "sub_category": self.transaction_subcategory.category_name,
                }

            response = self.client.post(
                "/graphql/",
                json.dumps({"query": create_transaction, "variables": variables}),
                content_type="application/json",
                HTTP_AUTHORIZATION=f"JWT {self.token}",
            )

    def tearDown(self) -> None:
        self.client.logout()

        self.plan.delete()

        self.test_username = None

        self.token = None

        self.account_id = None

        self.business_activity.delete()

        self.transaction_group.delete()

        self.transaction_category.delete()

        self.transaction_subcategory.delete()

        self.transaction_type_payable.delete()

        self.transaction_type_receivable.delete()


class TestAppQueries(TestCase):
    def setUp(self) -> None:
        self.client = Client()

        self.plan = Plan.objects.create(name="Free")

        create_user_variables = {
            "email": "example@gmail.com",
            "first_name": "Test",
            "last_name": "User",
            "password": "#TestUser15",
            "password2": "#TestUser15",
        }

        response = self.client.post(
            "/graphql/",
            json.dumps(
                {
                    "query": create_user,
                    "variables": create_user_variables,
                }
            ),
            content_type="application/json",
        )

        self.test_username = response.json()["data"]["createUser"]["username"]

        token_auth_variables = {
            "username": self.test_username,
            "password": "#TestUser15",
        }

        get_token = self.client.post(
            "/graphql/",
            json.dumps({"query": token_auth, "variables": token_auth_variables}),
            content_type="application/json",
        )

        self.token = get_token.json()["data"]["tokenAuth"]["token"]

        self.business_activity = BusinessActivity.objects.create(
            name="Operating Activity"
        )

        self.transaction_group = TransactionGroup.objects.create(
            activity=self.business_activity, group_name="Revenue Transactions"
        )

        self.transaction_category = TransactionCategory.objects.create(
            parent=self.transaction_group,
            category_name="Sales",
            category_description="Sales category",
        )
        self.transaction_subcategory = TransactionSubCategory.objects.create(
            parent=self.transaction_category,
            category_name="Product sales",
            category_description="Sales subcategory",
        )

        self.transaction_type_payable = TransactionType.objects.create(
            type_name="payable",
            type_description="Payable description",
        )
        self.transaction_type_receivable = TransactionType.objects.create(
            type_name="receivable",
            type_description="Receivable description",
        )

        variables = {
            "account_name": "KCB test account",
            "account_type": "Savings",
            "account_balance": "20000.00",
            "currency_code": "USD",
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": create_account, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        self.account_id = data["data"]["createAccount"]["id"]

        for i in range(6):
            random_number = random.randint(1, 100)

            if random_number % 2 == 0:
                variables = {
                    "account_id": self.account_id,
                    "transaction_type": self.transaction_type_receivable.type_name,
                    "transaction_amount": "2500.00",
                    "transaction_date": "2023-04-22T13:30",
                    "description": "Test transaction receivable",
                    "category": self.transaction_category.category_name,
                    "sub_category": self.transaction_subcategory.category_name,
                }

            else:
                variables = {
                    "account_id": self.account_id,
                    "transaction_type": self.transaction_type_payable.type_name,
                    "transaction_amount": "1500.00",
                    "transaction_date": "2023-04-20T15:30",
                    "description": "Test transaction payable",
                    "category": self.transaction_category.category_name,
                    "sub_category": self.transaction_subcategory.category_name,
                }

            response = self.client.post(
                "/graphql/",
                json.dumps({"query": create_transaction, "variables": variables}),
                content_type="application/json",
                HTTP_AUTHORIZATION=f"JWT {self.token}",
            )

    def tearDown(self) -> None:
        self.client.logout()

        self.plan.delete()

        self.test_username = None

        self.token = None

        self.account_id = None

        self.business_activity.delete()

        self.transaction_group.delete()

        self.transaction_category.delete()

        self.transaction_subcategory.delete()

        self.transaction_type_payable.delete()

        self.transaction_type_receivable.delete()
