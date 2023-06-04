import json
import random
from plans.models import Plan
from django.test import TestCase, Client
from reports.models import BusinessActivity
from controls.test_ref import explain_status_code
from transactions.models import (
    TransactionType,
    TransactionGroup,
    TransactionCategory,
    TransactionSubCategory,
)

from controls.mutation_ref import (
    token_auth,
    create_user,
    delete_report,
    create_account,
    generate_report,
    create_transaction,
)
from controls.query_ref import get_all_reports, get_report


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

    def test_generate_report(self):
        variables = {
            "account_id": self.account_id,
            "begin_date": "2023-04-15T00:00",
            "end_date": "2023-04-30T00:00",
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": generate_report, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            f"Something went wrong, {explain_status_code(response.status_code)}",
        )

        self.assertEqual(len(data["data"]["generateReport"]), 2)
        self.assertEqual(
            data["data"]["generateReport"][0]["statement_uid"],
            data["data"]["generateReport"][1]["statement_uid"],
        )
        self.assertEqual(
            data["data"]["generateReport"][0]["item"]["name"],
            f"{self.transaction_category}-{self.transaction_subcategory}",
        )
        self.assertEqual(
            data["data"]["generateReport"][1]["item"]["name"],
            f"{self.transaction_category}-{self.transaction_subcategory}",
        )
        self.assertEqual(data["data"]["generateReport"][0]["item"]["is_income"], False)
        self.assertEqual(data["data"]["generateReport"][1]["item"]["is_income"], True)

    def test_delete_report(self):
        variables = {
            "account_id": self.account_id,
            "begin_date": "2023-04-15T00:00",
            "end_date": "2023-04-30T00:00",
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": generate_report, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        variables = {
            "statement_uid": data["data"]["generateReport"][0]["statement_uid"]
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": delete_report, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            f"Something went wrong, {explain_status_code(response.status_code)}",
        )

        self.assertEqual(data["data"]["deleteReport"], True)


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

    def test_get_all_records(self):
        variables = {
            "account_id": self.account_id,
            "begin_date": "2023-04-15T00:00",
            "end_date": "2023-04-30T00:00",
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": generate_report, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        variables = {"account_id": self.account_id}

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": get_all_reports, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            f"Something went wrong, {explain_status_code(response.status_code)}",
        )

        self.assertEqual(type(data["data"]["getAllReports"]), type([]))
        self.assertIsNotNone(data["data"]["getAllReports"][0]["statement_uid"])
        self.assertEqual(data["data"]["getAllReports"][0]["begin_date"], "1681516800.0")
        self.assertEqual(data["data"]["getAllReports"][0]["end_date"], "1682812800.0")

    def test_get_record(self):
        variables = {
            "account_id": self.account_id,
            "begin_date": "2023-04-15T00:00",
            "end_date": "2023-04-30T00:00",
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": generate_report, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        variables = {
            "statement_uid": data["data"]["generateReport"][0]["statement_uid"]
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": get_report, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            f"Something went wrong, {explain_status_code(response.status_code)}",
        )

        self.assertEqual(len(data["data"]["getReport"]), 2)
        self.assertEqual(
            data["data"]["getReport"][0]["statement_uid"],
            data["data"]["getReport"][1]["statement_uid"],
        )
        self.assertEqual(
            data["data"]["getReport"][0]["item"]["name"],
            f"{self.transaction_category}-{self.transaction_subcategory}",
        )
        self.assertEqual(
            data["data"]["getReport"][1]["item"]["name"],
            f"{self.transaction_category}-{self.transaction_subcategory}",
        )
        self.assertEqual(data["data"]["getReport"][0]["item"]["is_income"], False)
        self.assertEqual(data["data"]["getReport"][1]["item"]["is_income"], True)
