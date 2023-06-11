import json
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
    update_transaction,
    delete_transaction,
)
from controls.query_ref import get_all_transactions, get_transaction


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

    def tearDown(self):
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

    def test_create_transaction(self):
        variables = {
            "account_id": self.account_id,
            "transaction_type": self.transaction_type_receivable.type_name,
            "transaction_amount": "2500.00",
            "transaction_date": "2023-04-22T13:30",
            "description": "Test transaction description",
            "category": self.transaction_category.category_name,
            "sub_category": self.transaction_subcategory.category_name,
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": create_transaction, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        self.assertEqual(
            data["data"]["createTransaction"]["transaction_type"]["type_name"],
            "receivable",
        )
        self.assertEqual(
            data["data"]["createTransaction"]["transaction_amount"], 2500.00
        )
        self.assertEqual(
            data["data"]["createTransaction"]["transaction_date"], "1682170200.0"
        )
        self.assertEqual(
            data["data"]["createTransaction"]["account"]["account_balance"], 22500.00
        )

    def test_update_transaction(self):
        variables = {
            "account_id": self.account_id,
            "transaction_type": self.transaction_type_receivable.type_name,
            "transaction_amount": "2500.00",
            "transaction_date": "2023-04-22T13:30",
            "description": "Test transaction description",
            "category": self.transaction_category.category_name,
            "sub_category": self.transaction_subcategory.category_name,
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": create_transaction, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        transaction_id = data["data"]["createTransaction"]["id"]

        variables = {
            "id": transaction_id,
            "account_id": self.account_id,
            "transaction_type": self.transaction_type_payable.type_name,
            "transaction_amount": "3500.00",
            "transaction_date": "2023-03-20T15:30",
            "description": "Test transaction update",
            "category": self.transaction_category.category_name,
            "sub_category": self.transaction_subcategory.category_name,
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": update_transaction, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            f"Something went wrong, {explain_status_code(response.status_code)}",
        )

        self.assertEqual(
            data["data"]["updateTransaction"]["transaction_type"]["type_name"],
            "payable",
        )
        self.assertEqual(
            data["data"]["updateTransaction"]["transaction_amount"], 3500.00
        )
        self.assertEqual(
            data["data"]["updateTransaction"]["transaction_date"], "1679326200.0"
        )
        self.assertEqual(
            data["data"]["updateTransaction"]["account"]["account_balance"], 16500.00
        )

    def test_delete_transaction(self):
        variables = {
            "account_id": self.account_id,
            "transaction_type": self.transaction_type_receivable.type_name,
            "transaction_amount": "2500.00",
            "transaction_date": "2023-04-22T13:30",
            "description": "Test transaction description",
            "category": self.transaction_category.category_name,
            "sub_category": self.transaction_subcategory.category_name,
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": create_transaction, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        variables = {
            "id": data["data"]["createTransaction"]["id"],
            "account_id": self.account_id,
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": delete_transaction, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            f"Something went wrong, {explain_status_code(response.status_code)}",
        )

        self.assertEqual(data["data"]["deleteTransaction"], True)


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

        variables = {
            "account_id": self.account_id,
            "transaction_type": self.transaction_type_receivable.type_name,
            "transaction_amount": "2500.00",
            "transaction_date": "2023-04-22T13:30",
            "description": "Test transaction description",
            "category": self.transaction_category.category_name,
            "sub_category": self.transaction_subcategory.category_name,
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": create_transaction, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        self.transaction_id = data["data"]["createTransaction"]["id"]

    def tearDown(self) -> None:
        self.client.logout()

        self.plan.delete()

        self.test_username = None

        self.token = None

        self.account_id = None

        self.transaction_id = None

        self.business_activity.delete()

        self.transaction_group.delete()

        self.transaction_category.delete()

        self.transaction_subcategory.delete()

        self.transaction_type_payable.delete()

        self.transaction_type_receivable.delete()

    def test_get_all_transactions(self):
        variables = {"account_id": self.account_id}

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": get_all_transactions, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            f"Something went wrong, {explain_status_code(response.status_code)}",
        )

        self.assertEqual(
            data["data"]["getAllTransactions"][0]["transaction_type"]["type_name"],
            "receivable",
        )
        self.assertEqual(
            data["data"]["getAllTransactions"][0]["transaction_amount"], 2500.00
        )
        self.assertEqual(
            data["data"]["getAllTransactions"][0]["transaction_date"], "1682159400.0"
        )
        self.assertEqual(
            data["data"]["getAllTransactions"][0]["account"]["account_balance"],
            22500.00,
        )

    def test_get_transaction(self):
        variables = {"id": self.transaction_id}

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": get_transaction, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            f"Something went wrong, {explain_status_code(response.status_code)}",
        )

        self.assertEqual(
            data["data"]["getTransaction"]["transaction_type"]["type_name"],
            "receivable",
        )
        self.assertEqual(data["data"]["getTransaction"]["transaction_amount"], 2500.00)
        self.assertEqual(
            data["data"]["getTransaction"]["transaction_date"], "1682159400.0"
        )
        self.assertEqual(
            data["data"]["getTransaction"]["account"]["account_balance"],
            22500.00,
        )
