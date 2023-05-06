import json
from plans.models import Plan
from django.test import TestCase, Client
from controls.test_ref import explain_status_code
from transactions.models import (
    TransactionType,
    TransactionCategory,
    TransactionSubCategory,
)

from controls.mutation_ref import (
    token_auth,
    create_user,
    create_target,
    update_target,
    target_status,
    delete_target,
    create_account,
)
from controls.query_ref import get_all_targets, get_target


class TestAppMutations(TestCase):
    def setUp(self) -> None:
        self.client = Client()

        self.plan = Plan.objects.create(name="Free")

        create_user_variables = {
            "email": "example@gmail.com",
            "first_name": "Test",
            "last_name": "User",
            "workspace_name": "Important Workspace",
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

        self.transaction_category = TransactionCategory.objects.create(
            category_name="Sales", category_description="Sales category"
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
            "account_balance": 20000.00,
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

    def tearDown(self) -> None:
        self.client.logout()

        self.plan.delete()

        self.test_username = None

        self.token = None

        self.account_id = None

    def test_create_target(self):
        variables = {
            "account_id": self.account_id,
            "target_name": "Test target",
            "target_description": "Test target description",
            "target_amount": 5000.00,
            "category": self.transaction_category.category_name,
            "sub_category": self.transaction_subcategory.category_name,
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": create_target, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            f"Something went wrong, {explain_status_code(response.status_code)}",
        )

        self.assertEqual(data["data"]["createTarget"]["target_name"], "Test target")
        self.assertEqual(
            data["data"]["createTarget"]["target_description"],
            "Test target description",
        )
        self.assertEqual(data["data"]["createTarget"]["target_amount"], 5000.00)
        self.assertEqual(data["data"]["createTarget"]["target_is_active"], True)
        self.assertEqual(
            data["data"]["createTarget"]["category"]["category_name"], "Sales"
        )
        self.assertEqual(
            data["data"]["createTarget"]["sub_category"]["category_name"],
            "Product sales",
        )

    def test_update_target(self):
        variables = {
            "account_id": self.account_id,
            "target_name": "Test target",
            "target_description": "Test target description",
            "target_amount": 5000.00,
            "category": self.transaction_category.category_name,
            "sub_category": self.transaction_subcategory.category_name,
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": create_target, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        variables = {
            "id": data["data"]["createTarget"]["id"],
            "target_name": "New target",
            "target_description": "New target description",
            "target_amount": 2500.00,
            "category": self.transaction_category.category_name,
            "sub_category": self.transaction_subcategory.category_name,
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": update_target, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            f"Something went wrong, {explain_status_code(response.status_code)}",
        )

        self.assertEqual(data["data"]["updateTarget"]["target_name"], "New target")
        self.assertEqual(
            data["data"]["updateTarget"]["target_description"],
            "New target description",
        )
        self.assertEqual(data["data"]["updateTarget"]["target_amount"], 2500.00)

    def test_delete_target(self):
        variables = {
            "account_id": self.account_id,
            "target_name": "Test target",
            "target_description": "Test target description",
            "target_amount": 5000.00,
            "category": self.transaction_category.category_name,
            "sub_category": self.transaction_subcategory.category_name,
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": create_target, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        variables = {"id": data["data"]["createTarget"]["id"]}

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": delete_target, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            f"Something went wrong, {explain_status_code(response.status_code)}",
        )

        self.assertEqual(data["data"]["deleteTarget"], True)

class TestAppQueries(TestCase):
    def setUp(self) -> None:
        self.client = Client()

        self.plan = Plan.objects.create(name="Free")

        create_user_variables = {
            "email": "example@gmail.com",
            "first_name": "Test",
            "last_name": "User",
            "workspace_name": "Important Workspace",
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

        self.transaction_category = TransactionCategory.objects.create(
            category_name="Sales", category_description="Sales category"
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
            "account_balance": 20000.00,
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
            "target_name": "Test target",
            "target_description": "Test target description",
            "target_amount": 5000.00,
            "category": self.transaction_category.category_name,
            "sub_category": self.transaction_subcategory.category_name,
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": create_target, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        self.target_id = data["data"]["createTarget"]["id"]

    def tearDown(self) -> None:
        self.client.logout()

        self.plan.delete()

        self.test_username = None

        self.token = None

        self.account_id = None

        self.target_id = None

    def test_get_all_targets(self):
        variables = {}

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": get_all_targets, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            f"Something went wrong, {explain_status_code(response.status_code)}",
        )

        self.assertEqual(data["data"]["getAllTargets"][0]["target_name"], "Test target")
        self.assertEqual(
            data["data"]["getAllTargets"][0]["target_description"],
            "Test target description",
        )
        self.assertEqual(data["data"]["getAllTargets"][0]["target_amount"], 5000.00)
        self.assertEqual(data["data"]["getAllTargets"][0]["target_is_active"], True)
        self.assertEqual(
            data["data"]["getAllTargets"][0]["category"]["category_name"], "Sales"
        )
        self.assertEqual(
            data["data"]["getAllTargets"][0]["sub_category"]["category_name"],
            "Product sales",
        )

    def test_get_target(self):
        variables = {"id": self.target_id}

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": get_target, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            f"Something went wrong, {explain_status_code(response.status_code)}",
        )

        self.assertEqual(data["data"]["getTarget"]["target_name"], "Test target")
        self.assertEqual(
            data["data"]["getTarget"]["target_description"],
            "Test target description",
        )
        self.assertEqual(data["data"]["getTarget"]["target_amount"], 5000.00)
        self.assertEqual(data["data"]["getTarget"]["target_is_active"], True)
        self.assertEqual(
            data["data"]["getTarget"]["category"]["category_name"], "Sales"
        )
        self.assertEqual(
            data["data"]["getTarget"]["sub_category"]["category_name"],
            "Product sales",
        )

    