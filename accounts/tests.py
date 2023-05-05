import json
from plans.models import Plan
from django.test import TestCase, Client
from controls.test_ref import explain_status_code

from controls.mutation_ref import (
    create_user,
    token_auth,
    create_account,
    update_account,
    delete_account,
)
from controls.query_ref import get_all_accounts, get_account


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

    def tearDown(self) -> None:
        self.client.logout()

        self.plan.delete()

        self.test_username = None

        self.token = None

    def test_create_account(self):
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

        self.assertEqual(
            response.status_code,
            200,
            f"Something went wrong, {explain_status_code(response.status_code)}",
        )

        self.assertEqual(data["data"]["createAccount"]["account_type"], "Savings")
        self.assertEqual(data["data"]["createAccount"]["account_balance"], 20000.00)
        self.assertEqual(data["data"]["createAccount"]["currency_code"], "USD")
        self.assertEqual(
            data["data"]["createAccount"]["account_name"], "KCB test account"
        )

    def test_update_account(self):
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

        variables = {
            "id": data["data"]["createAccount"]["id"],
            "account_name": "Equity test account",
            "account_type": "Checking",
            "account_balance": 25000.00,
            "currency_code": "KES",
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": update_account, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            f"Something went wrong, {explain_status_code(response.status_code)}",
        )

        self.assertEqual(data["data"]["updateAccount"]["account_type"], "Checking")
        self.assertEqual(data["data"]["updateAccount"]["account_balance"], 25000.00)
        self.assertEqual(data["data"]["updateAccount"]["currency_code"], "KES")
        self.assertEqual(
            data["data"]["updateAccount"]["account_name"], "Equity test account"
        )

    def test_delete_account(self):
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

        variables = {"id": data["data"]["createAccount"]["id"]}

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": delete_account, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            f"Something went wrong, {explain_status_code(response.status_code)}",
        )

        self.assertEqual(data["data"]["deleteAccount"], True)


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

    def test_get_all_accounts(self):
        variables = {}

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": get_all_accounts, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            f"Something went wrong, {explain_status_code(response.status_code)}",
        )

        self.assertEqual(data["data"]["getAllAccounts"][0]["account_type"], "Savings")
        self.assertEqual(data["data"]["getAllAccounts"][0]["account_balance"], 20000.00)
        self.assertEqual(data["data"]["getAllAccounts"][0]["currency_code"], "USD")
        self.assertEqual(
            data["data"]["getAllAccounts"][0]["account_name"], "KCB test account"
        )

    def test_get_account(self):
        variables = {"id": self.account_id}

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": get_account, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            f"Something went wrong, {explain_status_code(response.status_code)}",
        )

        self.assertEqual(data["data"]["getAccount"]["account_type"], "Savings")
        self.assertEqual(data["data"]["getAccount"]["account_balance"], 20000.00)
        self.assertEqual(data["data"]["getAccount"]["currency_code"], "USD")
        self.assertEqual(data["data"]["getAccount"]["account_name"], "KCB test account")

    
