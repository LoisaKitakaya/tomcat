import json
from plans.models import Plan
from debts.models import Customer, Debt
from django.test import TestCase, Client
from controls.test_ref import explain_status_code

from controls.mutation_ref import (
    create_user,
    token_auth,
    record_debt,
    update_debt,
    delete_debt,
    create_account,
    create_customer,
    update_customer,
    delete_customer,
)
from controls.query_ref import get_all_customers, get_customer, get_all_debts, get_debt


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

    def test_create_customer(self):
        variables = {
            "account_id": self.account_id,
            "name": "Test Customer",
            "email": "test@example.com",
            "phone": "+254712345678",
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": create_customer, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            f"Something went wrong, {explain_status_code(response.status_code)}",
        )

        self.assertEqual(data["data"]["createCustomer"]["name"], "Test Customer")
        self.assertEqual(data["data"]["createCustomer"]["email"], "test@example.com")
        self.assertEqual(data["data"]["createCustomer"]["phone"], "+254712345678")

    def test_update_customer(self):
        variables = {
            "account_id": self.account_id,
            "name": "Test Customer",
            "email": "test@example.com",
            "phone": "+254712345678",
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": create_customer, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        variables = {
            "id": data["data"]["createCustomer"]["id"],
            "name": "Update Customer",
            "email": "test@update.com",
            "phone": "+254787654321",
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": update_customer, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            f"Something went wrong, {explain_status_code(response.status_code)}",
        )

        self.assertEqual(data["data"]["updateCustomer"]["name"], "Update Customer")
        self.assertEqual(data["data"]["updateCustomer"]["email"], "test@update.com")
        self.assertEqual(data["data"]["updateCustomer"]["phone"], "+254787654321")

    def test_delete_customer(self):
        variables = {
            "account_id": self.account_id,
            "name": "Test Customer",
            "email": "test@example.com",
            "phone": "+254712345678",
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": create_customer, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        variables = {"id": data["data"]["createCustomer"]["id"]}

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": delete_customer, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            f"Something went wrong, {explain_status_code(response.status_code)}",
        )

        self.assertEqual(data["data"]["deleteCustomer"], True)

    def test_create_debt(self):
        variables = {
            "account_id": self.account_id,
            "name": "Test Customer",
            "email": "test@example.com",
            "phone": "+254712345678",
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": create_customer, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        customer_id = data["data"]["createCustomer"]["id"]

        variables = {
            "account_id": self.account_id,
            "customer_id": customer_id,
            "amount": 250.00,
            "due_date": "2023-04-22",
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": record_debt, "variables": variables}),
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
            data["data"]["recordDebt"]["customer"]["name"], "Test Customer"
        )
        self.assertEqual(data["data"]["recordDebt"]["amount"], 250.00)
        self.assertEqual(data["data"]["recordDebt"]["due_date"], "1682110800.0")
        self.assertEqual(data["data"]["recordDebt"]["is_paid"], False)

    def test_update_debt(self):
        variables = {
            "account_id": self.account_id,
            "name": "Test Customer",
            "email": "test@example.com",
            "phone": "+254712345678",
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": create_customer, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        customer_id = data["data"]["createCustomer"]["id"]

        variables = {
            "account_id": self.account_id,
            "customer_id": customer_id,
            "amount": 250.00,
            "due_date": "2023-04-22",
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": record_debt, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        variables = {
            "id": data["data"]["recordDebt"]["id"],
            "amount": 200.00,
            "due_date": "2023-04-22",
            "is_paid": True,
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": update_debt, "variables": variables}),
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
            data["data"]["updateDebt"]["customer"]["name"], "Test Customer"
        )
        self.assertEqual(data["data"]["updateDebt"]["amount"], 200.00)
        self.assertEqual(data["data"]["updateDebt"]["due_date"], "1682110800.0")
        self.assertEqual(data["data"]["updateDebt"]["is_paid"], True)

    def test_delete_debt(self):
        variables = {
            "account_id": self.account_id,
            "name": "Test Customer",
            "email": "test@example.com",
            "phone": "+254712345678",
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": create_customer, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        customer_id = data["data"]["createCustomer"]["id"]

        variables = {
            "account_id": self.account_id,
            "customer_id": customer_id,
            "amount": 250.00,
            "due_date": "2023-04-22",
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": record_debt, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        variables = {"id": data["data"]["recordDebt"]["id"]}

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": delete_debt, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            f"Something went wrong, {explain_status_code(response.status_code)}",
        )

        self.assertEqual(data["data"]["deleteDebt"], True)


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

        variables = {
            "account_id": self.account_id,
            "name": "Test Customer",
            "email": "test@example.com",
            "phone": "+254712345678",
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": create_customer, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        self.customer_id = data["data"]["createCustomer"]["id"]

        variables = {
            "account_id": self.account_id,
            "customer_id": self.customer_id,
            "amount": 250.00,
            "due_date": "2023-04-22",
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": record_debt, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        self.debt_id = data["data"]["recordDebt"]["id"]

    def tearDown(self) -> None:
        self.client.logout()

        self.plan.delete()

        self.test_username = None

        self.token = None

        self.account_id = None

        self.customer_id = None

        self.debt_id = None

    def test_get_all_customers(self):
        variables = {"account_id": self.account_id}

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": get_all_customers, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            f"Something went wrong, {explain_status_code(response.status_code)}",
        )

        self.assertEqual(data["data"]["getAllCustomers"][0]["name"], "Test Customer")
        self.assertEqual(
            data["data"]["getAllCustomers"][0]["email"], "test@example.com"
        )
        self.assertEqual(data["data"]["getAllCustomers"][0]["phone"], "+254712345678")

    def test_get_customer(self):
        variables = {"id": self.customer_id}

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": get_customer, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            f"Something went wrong, {explain_status_code(response.status_code)}",
        )

        self.assertEqual(data["data"]["getCustomer"]["name"], "Test Customer")
        self.assertEqual(data["data"]["getCustomer"]["email"], "test@example.com")
        self.assertEqual(data["data"]["getCustomer"]["phone"], "+254712345678")

    def test_get_all_debts(self):
        variables = {"account_id": self.account_id}

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": get_all_debts, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            f"Something went wrong, {explain_status_code(response.status_code)}",
        )

        self.assertEqual(data["data"]["getAllDebts"][0]["amount"], 250.00)
        self.assertEqual(data["data"]["getAllDebts"][0]["due_date"], "1682110800.0")
        self.assertEqual(data["data"]["getAllDebts"][0]["is_paid"], False)

    def test_get_debt(self):
        variables = {"id": self.debt_id}

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": get_debt, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            f"Something went wrong, {explain_status_code(response.status_code)}",
        )

        self.assertEqual(data["data"]["getDebt"]["amount"], 250.00)
        self.assertEqual(data["data"]["getDebt"]["due_date"], "1682110800.0")
        self.assertEqual(data["data"]["getDebt"]["is_paid"], False)
