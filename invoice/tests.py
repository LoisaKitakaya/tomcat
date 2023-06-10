import json
from plans.models import Plan
from django.test import TestCase, Client
from controls.test_ref import explain_status_code
from transactions.models import (
    TransactionGroup,
    BusinessActivity,
    TransactionCategory,
    TransactionSubCategory,
)

from controls.query_ref import (
    get_invoice,
    get_all_invoices,
    get_payment_account,
    get_client_information,
    get_all_payment_accounts,
    get_all_client_information,
)
from controls.mutation_ref import (
    token_auth,
    create_user,
    create_invoice,
    update_invoice,
    delete_invoice,
    create_payment_account,
    update_payment_account,
    delete_payment_account,
    create_client_information,
    update_client_information,
    delete_client_information,
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

    def tearDown(self) -> None:
        self.client.logout()

        self.plan.delete()

        self.test_username = None

        self.token = None

        self.business_activity.delete()

        self.transaction_group.delete()

        self.transaction_category.delete()

        self.transaction_subcategory.delete()

    def test_create_payment_account(self):
        variables = {
            "business_name": "Test Payment Account",
            "business_email": "test@example.com",
            "business_phone_number": "+25412345679",
            "bank_name": "Test Bank Account",
            "bank_account": "10302938420384",
            "mobile_payment_name": "Test Mobile Payment Account",
            "mobile_account": "2342342",
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": create_payment_account, "variables": variables}),
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
            data["data"]["createPaymentAccount"]["business_name"],
            "Test Payment Account",
        )
        self.assertEqual(
            data["data"]["createPaymentAccount"]["business_email"], "test@example.com"
        )
        self.assertEqual(
            data["data"]["createPaymentAccount"]["business_phone_number"],
            "+25412345679",
        )
        self.assertEqual(
            data["data"]["createPaymentAccount"]["bank_name"], "Test Bank Account"
        )
        self.assertEqual(
            data["data"]["createPaymentAccount"]["bank_account"], "10302938420384"
        )
        self.assertEqual(
            data["data"]["createPaymentAccount"]["mobile_payment_name"],
            "Test Mobile Payment Account",
        )
        self.assertEqual(
            data["data"]["createPaymentAccount"]["mobile_account"], "2342342"
        )

    def test_update_payment_account(self):
        variables = {
            "business_name": "Test Payment Account",
            "business_email": "test@example.com",
            "business_phone_number": "+25412345679",
            "bank_name": "Test Bank Account",
            "bank_account": "10302938420384",
            "mobile_payment_name": "Test Mobile Payment Account",
            "mobile_account": "2342342",
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": create_payment_account, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        variables = {
            "id": data["data"]["createPaymentAccount"]["id"],
            "business_name": "New Payment Account",
            "business_email": "",
            "business_phone_number": "",
            "bank_name": "New Bank Account",
            "bank_account": "",
            "mobile_payment_name": "New Mobile Payment Account",
            "mobile_account": "",
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": update_payment_account, "variables": variables}),
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
            data["data"]["updatePaymentAccount"]["business_name"], "New Payment Account"
        )
        self.assertEqual(
            data["data"]["updatePaymentAccount"]["business_email"], "test@example.com"
        )
        self.assertEqual(
            data["data"]["updatePaymentAccount"]["business_phone_number"],
            "+25412345679",
        )
        self.assertEqual(
            data["data"]["updatePaymentAccount"]["bank_name"], "New Bank Account"
        )
        self.assertEqual(
            data["data"]["updatePaymentAccount"]["bank_account"], "10302938420384"
        )
        self.assertEqual(
            data["data"]["updatePaymentAccount"]["mobile_payment_name"],
            "New Mobile Payment Account",
        )
        self.assertEqual(
            data["data"]["updatePaymentAccount"]["mobile_account"], "2342342"
        )

    def test_delete_payment_account(self):
        variables = {
            "business_name": "Test Payment Account",
            "business_email": "test@example.com",
            "business_phone_number": "+25412345679",
            "bank_name": "Test Bank Account",
            "bank_account": "10302938420384",
            "mobile_payment_name": "Test Mobile Payment Account",
            "mobile_account": "2342342",
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": create_payment_account, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        variables = {"id": data["data"]["createPaymentAccount"]["id"]}

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": delete_payment_account, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            f"Something went wrong, {explain_status_code(response.status_code)}",
        )

        self.assertEqual(data["data"]["deletePaymentAccount"], True)

    def test_create_client_information(self):
        variables = {
            "client_name": "Test Client Name",
            "client_email": "test@example.com",
            "client_phone_number": "+25412345679",
            "client_address": "2342342",
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": create_client_information, "variables": variables}),
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
            data["data"]["createClientInformation"]["client_name"], "Test Client Name"
        )
        self.assertEqual(
            data["data"]["createClientInformation"]["client_email"], "test@example.com"
        )
        self.assertEqual(
            data["data"]["createClientInformation"]["client_phone_number"],
            "+25412345679",
        )
        self.assertEqual(
            data["data"]["createClientInformation"]["client_address"], "2342342"
        )

    def test_update_client_information(self):
        variables = {
            "client_name": "Test Client Name",
            "client_email": "test@example.com",
            "client_phone_number": "+25412345679",
            "client_address": "2342342",
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": create_client_information, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        variables = {
            "id": data["data"]["createClientInformation"]["id"],
            "client_name": "New Client Name",
            "client_email": "",
            "client_phone_number": "+25412345678",
            "client_address": "",
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": update_client_information, "variables": variables}),
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
            data["data"]["updateClientInformation"]["client_name"], "New Client Name"
        )
        self.assertEqual(
            data["data"]["updateClientInformation"]["client_email"], "test@example.com"
        )
        self.assertEqual(
            data["data"]["updateClientInformation"]["client_phone_number"],
            "+25412345678",
        )
        self.assertEqual(
            data["data"]["updateClientInformation"]["client_address"], "2342342"
        )

    def test_delete_client_information(self):
        variables = {
            "client_name": "Test Client Name",
            "client_email": "test@example.com",
            "client_phone_number": "+25412345679",
            "client_address": "2342342",
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": create_client_information, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        variables = {"id": data["data"]["createClientInformation"]["id"]}

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": delete_client_information, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            f"Something went wrong, {explain_status_code(response.status_code)}",
        )

        self.assertEqual(data["data"]["deleteClientInformation"], True)

    def test_create_invoice(self):
        variables = {
            "business_name": "Test Payment Account 1",
            "business_email": "test@example.com",
            "business_phone_number": "+25412345679",
            "bank_name": "Test Bank Account",
            "bank_account": "10302938420384",
            "mobile_payment_name": "Test Mobile Payment Account",
            "mobile_account": "2342342",
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": create_payment_account, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        payment_account = data["data"]["createPaymentAccount"]["business_name"]

        variables = {
            "client_name": "Test Client Name 1",
            "client_email": "test@example.com",
            "client_phone_number": "+25412345679",
            "client_address": "2342342",
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": create_client_information, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        client_information = data["data"]["createClientInformation"]["client_name"]

        variables = {
            "business": payment_account,
            "client": client_information,
            "category": self.transaction_category.category_name,
            "sub_category": self.transaction_subcategory.category_name,
            "item": "Test Item",
            "quantity": "5",
            "amount": "200.00",
            "additional_notes": "Here are additional notes for this invoice.",
            "due_date": "2023-04-22T13:30",
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": create_invoice, "variables": variables}),
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
            data["data"]["createInvoice"]["business"]["business_name"],
            "Test Payment Account 1",
        )
        self.assertEqual(
            data["data"]["createInvoice"]["client"]["client_name"], "Test Client Name 1"
        )
        self.assertEqual(
            data["data"]["createInvoice"]["category"]["category_name"], "Sales"
        )
        self.assertEqual(
            data["data"]["createInvoice"]["sub_category"]["category_name"],
            "Product sales",
        )
        self.assertEqual(data["data"]["createInvoice"]["item"], "Test Item")
        self.assertEqual(data["data"]["createInvoice"]["quantity"], 5)
        self.assertEqual(data["data"]["createInvoice"]["amount"], 200)
        self.assertEqual(data["data"]["createInvoice"]["total"], 1000.00)
        self.assertEqual(
            data["data"]["createInvoice"]["additional_notes"],
            "Here are additional notes for this invoice.",
        )
        self.assertEqual(data["data"]["createInvoice"]["due_date"], "1682170200.0")

    def test_update_invoice(self):
        variables = {
            "business_name": "Test Payment Account 2",
            "business_email": "test@example.com",
            "business_phone_number": "+25412345679",
            "bank_name": "Test Bank Account",
            "bank_account": "10302938420384",
            "mobile_payment_name": "Test Mobile Payment Account",
            "mobile_account": "2342342",
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": create_payment_account, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        payment_account = data["data"]["createPaymentAccount"]["business_name"]

        variables = {
            "client_name": "Test Client Name 2",
            "client_email": "test@example.com",
            "client_phone_number": "+25412345679",
            "client_address": "2342342",
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": create_client_information, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        client_information = data["data"]["createClientInformation"]["client_name"]

        variables = {
            "business": payment_account,
            "client": client_information,
            "category": self.transaction_category.category_name,
            "sub_category": self.transaction_subcategory.category_name,
            "item": "Test Item",
            "quantity": "5",
            "amount": "200.00",
            "additional_notes": "Here are additional notes for this invoice.",
            "due_date": "2023-04-22T13:30",
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": create_invoice, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        variables = {
            "id": data["data"]["createInvoice"]["id"],
            "business": "",
            "client": "",
            "category": "",
            "sub_category": "",
            "item": "Updated Test Item",
            "quantity": "3",
            "amount": "",
            "additional_notes": "",
            "due_date": "",
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": update_invoice, "variables": variables}),
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
            data["data"]["updateInvoice"]["business"]["business_name"],
            "Test Payment Account 2",
        )
        self.assertEqual(
            data["data"]["updateInvoice"]["client"]["client_name"], "Test Client Name 2"
        )
        self.assertEqual(
            data["data"]["updateInvoice"]["category"]["category_name"], "Sales"
        )
        self.assertEqual(
            data["data"]["updateInvoice"]["sub_category"]["category_name"],
            "Product sales",
        )
        self.assertEqual(data["data"]["updateInvoice"]["item"], "Updated Test Item")
        self.assertEqual(data["data"]["updateInvoice"]["quantity"], 3)
        self.assertEqual(data["data"]["updateInvoice"]["amount"], 200)
        self.assertEqual(data["data"]["updateInvoice"]["total"], 600.00)
        self.assertEqual(
            data["data"]["updateInvoice"]["additional_notes"],
            "Here are additional notes for this invoice.",
        )
        self.assertEqual(data["data"]["updateInvoice"]["due_date"], "1682170200.0")

    def test_delete_invoice(self):
        variables = {
            "business_name": "Test Payment Account 3",
            "business_email": "test@example.com",
            "business_phone_number": "+25412345679",
            "bank_name": "Test Bank Account",
            "bank_account": "10302938420384",
            "mobile_payment_name": "Test Mobile Payment Account",
            "mobile_account": "2342342",
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": create_payment_account, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        payment_account = data["data"]["createPaymentAccount"]["business_name"]

        variables = {
            "client_name": "Test Client Name 3",
            "client_email": "test@example.com",
            "client_phone_number": "+25412345679",
            "client_address": "2342342",
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": create_client_information, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        client_information = data["data"]["createClientInformation"]["client_name"]

        variables = {
            "business": payment_account,
            "client": client_information,
            "category": self.transaction_category.category_name,
            "sub_category": self.transaction_subcategory.category_name,
            "item": "Test Item",
            "quantity": "5",
            "amount": "200.00",
            "additional_notes": "Here are additional notes for this invoice.",
            "due_date": "2023-04-22T13:30",
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": create_invoice, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        variables = {"id": data["data"]["createInvoice"]["id"]}

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": delete_invoice, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            f"Something went wrong, {explain_status_code(response.status_code)}",
        )

        self.assertEqual(data["data"]["deleteInvoice"], True)


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

        variables = {
            "business_name": "Test Payment Account",
            "business_email": "test@example.com",
            "business_phone_number": "+25412345679",
            "bank_name": "Test Bank Account",
            "bank_account": "10302938420384",
            "mobile_payment_name": "Test Mobile Payment Account",
            "mobile_account": "2342342",
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": create_payment_account, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        self.payment_account_id = data["data"]["createPaymentAccount"]["id"]

        self.payment_account = data["data"]["createPaymentAccount"]["business_name"]

        variables = {
            "client_name": "Test Client Name",
            "client_email": "test@example.com",
            "client_phone_number": "+25412345679",
            "client_address": "2342342",
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": create_client_information, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        self.client_information_id = data["data"]["createClientInformation"]["id"]

        self.client_information = data["data"]["createClientInformation"]["client_name"]

        variables = {
            "business": self.payment_account,
            "client": self.client_information,
            "category": self.transaction_category.category_name,
            "sub_category": self.transaction_subcategory.category_name,
            "item": "Test Item",
            "quantity": "5",
            "amount": "200.00",
            "additional_notes": "Here are additional notes for this invoice.",
            "due_date": "2023-04-22T13:30",
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": create_invoice, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        self.invoice_id = data["data"]["createInvoice"]["id"]

    def tearDown(self) -> None:
        self.client.logout()

        self.plan.delete()

        self.test_username = None

        self.token = None

        self.business_activity.delete()

        self.transaction_group.delete()

        self.transaction_category.delete()

        self.transaction_subcategory.delete()

        self.payment_account_id = None

        self.payment_account = None

        self.client_information_id = None

        self.client_information = None

        self.invoice_id = None

    def test_get_all_payment_accounts(self):
        variables = {}

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": get_all_payment_accounts, "variables": variables}),
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
            data["data"]["getAllPaymentAccounts"][0]["business_name"],
            "Test Payment Account",
        )
        self.assertEqual(
            data["data"]["getAllPaymentAccounts"][0]["business_email"],
            "test@example.com",
        )
        self.assertEqual(
            data["data"]["getAllPaymentAccounts"][0]["business_phone_number"],
            "+25412345679",
        )
        self.assertEqual(
            data["data"]["getAllPaymentAccounts"][0]["bank_name"], "Test Bank Account"
        )
        self.assertEqual(
            data["data"]["getAllPaymentAccounts"][0]["bank_account"], "10302938420384"
        )
        self.assertEqual(
            data["data"]["getAllPaymentAccounts"][0]["mobile_payment_name"],
            "Test Mobile Payment Account",
        )
        self.assertEqual(
            data["data"]["getAllPaymentAccounts"][0]["mobile_account"], "2342342"
        )

    def test_get_payment_account(self):
        variables = {"id": self.payment_account_id}

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": get_payment_account, "variables": variables}),
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
            data["data"]["getPaymentAccount"]["business_name"],
            "Test Payment Account",
        )
        self.assertEqual(
            data["data"]["getPaymentAccount"]["business_email"], "test@example.com"
        )
        self.assertEqual(
            data["data"]["getPaymentAccount"]["business_phone_number"],
            "+25412345679",
        )
        self.assertEqual(
            data["data"]["getPaymentAccount"]["bank_name"], "Test Bank Account"
        )
        self.assertEqual(
            data["data"]["getPaymentAccount"]["bank_account"], "10302938420384"
        )
        self.assertEqual(
            data["data"]["getPaymentAccount"]["mobile_payment_name"],
            "Test Mobile Payment Account",
        )
        self.assertEqual(data["data"]["getPaymentAccount"]["mobile_account"], "2342342")

    def test_get_all_client_information(self):
        variables = {}

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": get_all_client_information, "variables": variables}),
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
            data["data"]["getAllClientInformation"][0]["client_name"],
            "Test Client Name",
        )
        self.assertEqual(
            data["data"]["getAllClientInformation"][0]["client_email"],
            "test@example.com",
        )
        self.assertEqual(
            data["data"]["getAllClientInformation"][0]["client_phone_number"],
            "+25412345679",
        )
        self.assertEqual(
            data["data"]["getAllClientInformation"][0]["client_address"], "2342342"
        )

    def test_get_client_information(self):
        variables = {"id": self.client_information_id}

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": get_client_information, "variables": variables}),
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
            data["data"]["getClientInformation"]["client_name"], "Test Client Name"
        )
        self.assertEqual(
            data["data"]["getClientInformation"]["client_email"], "test@example.com"
        )
        self.assertEqual(
            data["data"]["getClientInformation"]["client_phone_number"],
            "+25412345679",
        )
        self.assertEqual(
            data["data"]["getClientInformation"]["client_address"], "2342342"
        )

    def test_get_all_invoices(self):
        variables = {}

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": get_all_invoices, "variables": variables}),
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
            data["data"]["getAllInvoices"][0]["business"]["business_name"],
            "Test Payment Account",
        )
        self.assertEqual(
            data["data"]["getAllInvoices"][0]["client"]["client_name"],
            "Test Client Name",
        )
        self.assertEqual(
            data["data"]["getAllInvoices"][0]["category"]["category_name"], "Sales"
        )
        self.assertEqual(
            data["data"]["getAllInvoices"][0]["sub_category"]["category_name"],
            "Product sales",
        )
        self.assertEqual(data["data"]["getAllInvoices"][0]["item"], "Test Item")
        self.assertEqual(data["data"]["getAllInvoices"][0]["quantity"], 5)
        self.assertEqual(data["data"]["getAllInvoices"][0]["amount"], 200)
        self.assertEqual(data["data"]["getAllInvoices"][0]["total"], 1000.00)
        self.assertEqual(
            data["data"]["getAllInvoices"][0]["additional_notes"],
            "Here are additional notes for this invoice.",
        )
        self.assertEqual(data["data"]["getAllInvoices"][0]["due_date"], "1682170200.0")

    def test_get_invoice(self):
        variables = {"id": self.invoice_id}

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": get_invoice, "variables": variables}),
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
            data["data"]["getInvoice"]["business"]["business_name"],
            "Test Payment Account",
        )
        self.assertEqual(
            data["data"]["getInvoice"]["client"]["client_name"], "Test Client Name"
        )
        self.assertEqual(
            data["data"]["getInvoice"]["category"]["category_name"], "Sales"
        )
        self.assertEqual(
            data["data"]["getInvoice"]["sub_category"]["category_name"],
            "Product sales",
        )
        self.assertEqual(data["data"]["getInvoice"]["item"], "Test Item")
        self.assertEqual(data["data"]["getInvoice"]["quantity"], 5)
        self.assertEqual(data["data"]["getInvoice"]["amount"], 200)
        self.assertEqual(data["data"]["getInvoice"]["total"], 1000.00)
        self.assertEqual(
            data["data"]["getInvoice"]["additional_notes"],
            "Here are additional notes for this invoice.",
        )
        self.assertEqual(data["data"]["getInvoice"]["due_date"], "1682170200.0")
