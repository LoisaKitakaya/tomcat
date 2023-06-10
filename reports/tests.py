import json
from plans.models import Plan
from django.test import TestCase, Client
from controls.test_ref import explain_status_code
from inventory.models import ProductCategory, ProductSubCategory
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
    create_product,
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

        self.product_category = ProductCategory.objects.create(
            category_name="Accessories",
            category_description="Accessories category",
        )

        self.product_subcategory = ProductSubCategory.objects.create(
            parent=self.product_category,
            category_name="Watches",
            category_description="Watches subcategory",
        )

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
            if i % 2 == 0:
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

        variables = {
            "account_id": self.account_id,
            "name": "Product One",
            "description": "This is a test product",
            "category": self.product_category.category_name,
            "sub_category": self.product_subcategory.category_name,
            "buying_price": "300.00",
            "selling_price": "500.00",
            "current_stock_level": "100",
            "units_sold": "20",
            "supplier_name": "Supplier",
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": create_product, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        variables = {
            "account_id": self.account_id,
            "name": "Product Two",
            "description": "This is another test product",
            "category": self.product_category.category_name,
            "sub_category": self.product_subcategory.category_name,
            "buying_price": "400.00",
            "selling_price": "600.00",
            "current_stock_level": "100",
            "units_sold": "50",
            "supplier_name": "Supplier",
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": create_product, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

    def tearDown(self) -> None:
        self.client.logout()

        self.plan.delete()

        self.test_username = None

        self.token = None

        self.account_id = None

        self.product_category.delete()

        self.product_subcategory.delete()

        self.business_activity.delete()

        self.transaction_group.delete()

        self.transaction_category.delete()

        self.transaction_subcategory.delete()

        self.transaction_type_payable.delete()

        self.transaction_type_receivable.delete()

    def test_generate_cash_flow_report(self):
        variables = {
            "account_id": self.account_id,
            "begin_date": "2023-04-20T15:30",
            "end_date": "2023-04-22T13:30",
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": generate_cash_flow_report, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            f"Something went wrong, {explain_status_code(response.status_code)}",
        )

        self.assertIsNotNone(data["data"]["generateCashFlowReport"]["uid"])
        self.assertEqual(type(data["data"]["generateCashFlowReport"]["uid"]), type(""))
        self.assertEqual(
            data["data"]["generateCashFlowReport"]["account"]["id"], self.account_id
        )
        self.assertEqual(
            data["data"]["generateCashFlowReport"]["period_start_date"], "1682004600.0"
        )
        self.assertEqual(
            data["data"]["generateCashFlowReport"]["period_end_date"], "1682170200.0"
        )

    def test_delete_cash_flow_report(self):
        variables = {
            "account_id": self.account_id,
            "begin_date": "2023-04-20T15:30",
            "end_date": "2023-04-22T13:30",
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": generate_cash_flow_report, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        variables = {"uid": data["data"]["generateCashFlowReport"]["uid"]}

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": delete_cash_flow_report, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            f"Something went wrong, {explain_status_code(response.status_code)}",
        )

        self.assertEqual(data["data"]["deleteCashFlowReport"], True)

    def test_generate_income_report(self):
        variables = {
            "account_id": self.account_id,
            "begin_date": "2023-04-20T15:30",
            "end_date": "2023-04-22T13:30",
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": generate_income_report, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            f"Something went wrong, {explain_status_code(response.status_code)}",
        )

        self.assertIsNotNone(data["data"]["generateIncomeReport"]["uid"])
        self.assertEqual(type(data["data"]["generateIncomeReport"]["uid"]), type(""))
        self.assertEqual(
            data["data"]["generateIncomeReport"]["account"]["id"], self.account_id
        )
        self.assertEqual(
            data["data"]["generateIncomeReport"]["period_start_date"], "1682004600.0"
        )
        self.assertEqual(
            data["data"]["generateIncomeReport"]["period_end_date"], "1682170200.0"
        )
        self.assertEqual(data["data"]["generateIncomeReport"]["revenue"], 7500.00)
        self.assertEqual(data["data"]["generateIncomeReport"]["gross_profit"], 21500.00)
        self.assertEqual(
            data["data"]["generateIncomeReport"]["operating_expenses"], 4500.00
        )
        self.assertEqual(data["data"]["generateIncomeReport"]["net_income"], 17000.00)

    def test_delete_income_report(self):
        variables = {
            "account_id": self.account_id,
            "begin_date": "2023-04-20T15:30",
            "end_date": "2023-04-22T13:30",
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": generate_income_report, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        variables = {"uid": data["data"]["generateIncomeReport"]["uid"]}

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": delete_income_report, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            f"Something went wrong, {explain_status_code(response.status_code)}",
        )

        self.assertEqual(data["data"]["deleteIncomeReport"], True)

    def test_generate_balance_sheet_report(self):
        variables = {
            "account_id": self.account_id,
            "assets": [
                {"item": "Asset One", "net_worth": "1000.00"},
                {"item": "Asset Two", "net_worth": "2000.00"},
                {"item": "Asset Three", "net_worth": "3000.00"},
            ],
            "liabilities": [
                {"item": "Liability One", "net_worth": "100.00"},
                {"item": "Liability Two", "net_worth": "200.00"},
                {"item": "Liability Three", "net_worth": "300.00"},
            ],
            "equity": [
                {"item": "Capital Investment One", "net_worth": "100.00"},
                {"item": "Capital Investment Two", "net_worth": "200.00"},
            ],
        }

        response = self.client.post(
            "/graphql/",
            json.dumps(
                {"query": generate_balance_sheet_report, "variables": variables}
            ),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            f"Something went wrong, {explain_status_code(response.status_code)}",
        )

        self.assertIsNotNone(data["data"]["generateBalanceSheetReport"]["uid"])
        self.assertEqual(
            type(data["data"]["generateBalanceSheetReport"]["uid"]), type("")
        )
        self.assertEqual(
            data["data"]["generateBalanceSheetReport"]["account"]["id"], self.account_id
        )
        self.assertEqual(data["data"]["generateBalanceSheetReport"]["assets"], 29000.00)
        self.assertEqual(
            data["data"]["generateBalanceSheetReport"]["liabilities"], 600.00
        )
        self.assertEqual(data["data"]["generateBalanceSheetReport"]["equity"], 28700.00)

    def test_delete_balance_sheet_report(self):
        variables = {
            "account_id": self.account_id,
            "assets": [
                {"item": "Asset One", "net_worth": "1000.00"},
                {"item": "Asset Two", "net_worth": "2000.00"},
                {"item": "Asset Three", "net_worth": "3000.00"},
            ],
            "liabilities": [
                {"item": "Liability One", "net_worth": "100.00"},
                {"item": "Liability Two", "net_worth": "200.00"},
                {"item": "Liability Three", "net_worth": "300.00"},
            ],
            "equity": [
                {"item": "Capital Investment One", "net_worth": "100.00"},
                {"item": "Capital Investment Two", "net_worth": "200.00"},
            ],
        }

        response = self.client.post(
            "/graphql/",
            json.dumps(
                {"query": generate_balance_sheet_report, "variables": variables}
            ),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        variables = {"uid": data["data"]["generateBalanceSheetReport"]["uid"]}

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": delete_balance_sheet_report, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            f"Something went wrong, {explain_status_code(response.status_code)}",
        )

        self.assertEqual(data["data"]["deleteBalanceSheetReport"], True)


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

        self.product_category = ProductCategory.objects.create(
            category_name="Accessories",
            category_description="Accessories category",
        )

        self.product_subcategory = ProductSubCategory.objects.create(
            parent=self.product_category,
            category_name="Watches",
            category_description="Watches subcategory",
        )

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
            if i % 2 == 0:
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

        variables = {
            "account_id": self.account_id,
            "name": "Product One",
            "description": "This is a test product",
            "category": self.product_category.category_name,
            "sub_category": self.product_subcategory.category_name,
            "buying_price": "300.00",
            "selling_price": "500.00",
            "current_stock_level": "100",
            "units_sold": "20",
            "supplier_name": "Supplier",
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": create_product, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        variables = {
            "account_id": self.account_id,
            "name": "Product Two",
            "description": "This is another test product",
            "category": self.product_category.category_name,
            "sub_category": self.product_subcategory.category_name,
            "buying_price": "400.00",
            "selling_price": "600.00",
            "current_stock_level": "100",
            "units_sold": "50",
            "supplier_name": "Supplier",
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": create_product, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

    def tearDown(self) -> None:
        self.client.logout()

        self.plan.delete()

        self.test_username = None

        self.token = None

        self.account_id = None

        self.product_category.delete()

        self.product_subcategory.delete()

        self.business_activity.delete()

        self.transaction_group.delete()

        self.transaction_category.delete()

        self.transaction_subcategory.delete()

        self.transaction_type_payable.delete()

        self.transaction_type_receivable.delete()

    def test_get_all_cash_flow_statements(self):
        variables = {
            "account_id": self.account_id,
            "begin_date": "2023-04-20T15:30",
            "end_date": "2023-04-22T13:30",
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": generate_cash_flow_report, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        variables = {"account_id": self.account_id}

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": get_all_cash_flow_statements, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            f"Something went wrong, {explain_status_code(response.status_code)}",
        )

        self.assertIsNotNone(data["data"]["getAllCashFlowStatements"][0]["uid"])
        self.assertEqual(
            type(data["data"]["getAllCashFlowStatements"][0]["uid"]), type("")
        )
        self.assertEqual(
            data["data"]["getAllCashFlowStatements"][0]["account"]["id"],
            self.account_id,
        )
        self.assertEqual(
            data["data"]["getAllCashFlowStatements"][0]["period_start_date"],
            "1681948800.0",
        )
        self.assertEqual(
            data["data"]["getAllCashFlowStatements"][0]["period_end_date"],
            "1682121600.0",
        )

    def test_get_cash_flow_statement(self):
        variables = {
            "account_id": self.account_id,
            "begin_date": "2023-04-20T15:30",
            "end_date": "2023-04-22T13:30",
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": generate_cash_flow_report, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        variables = {"uid": data["data"]["generateCashFlowReport"]["uid"]}

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": get_cash_flow_statement, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            f"Something went wrong, {explain_status_code(response.status_code)}",
        )

        self.assertIsNotNone(data["data"]["getCashFlowStatement"][0]["uid"])
        self.assertEqual(type(data["data"]["getCashFlowStatement"][0]["uid"]), type(""))
        self.assertEqual(
            data["data"]["getCashFlowStatement"][0]["account"]["id"], self.account_id
        )
        self.assertEqual(
            data["data"]["getCashFlowStatement"][0]["record"]["category"], "Sales"
        )
        self.assertEqual(
            data["data"]["getCashFlowStatement"][0]["record"]["item"], "Product sales"
        )
        self.assertEqual(
            data["data"]["getCashFlowStatement"][0]["record"]["activity"],
            "Operating Activity",
        )
        self.assertEqual(
            data["data"]["getCashFlowStatement"][0]["record"]["amount"], 7500.00
        )
        self.assertEqual(
            data["data"]["getCashFlowStatement"][0]["record"]["is_income"], True
        )
        self.assertEqual(
            data["data"]["getCashFlowStatement"][1]["record"]["category"], "Sales"
        )
        self.assertEqual(
            data["data"]["getCashFlowStatement"][1]["record"]["item"], "Product sales"
        )
        self.assertEqual(
            data["data"]["getCashFlowStatement"][1]["record"]["activity"],
            "Operating Activity",
        )
        self.assertEqual(
            data["data"]["getCashFlowStatement"][1]["record"]["amount"], 4500.00
        )
        self.assertEqual(
            data["data"]["getCashFlowStatement"][1]["record"]["is_income"], False
        )

    def test_get_all_income_statements(self):
        variables = {
            "account_id": self.account_id,
            "begin_date": "2023-04-20T15:30",
            "end_date": "2023-04-22T13:30",
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": generate_income_report, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        variables = {"account_id": self.account_id}

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": get_all_income_statements, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            f"Something went wrong, {explain_status_code(response.status_code)}",
        )

        self.assertIsNotNone(data["data"]["getAllIncomeStatements"][0]["uid"])
        self.assertEqual(
            type(data["data"]["getAllIncomeStatements"][0]["uid"]), type("")
        )
        self.assertEqual(
            data["data"]["getAllIncomeStatements"][0]["account"]["id"], self.account_id
        )
        self.assertEqual(
            data["data"]["getAllIncomeStatements"][0]["period_start_date"],
            "1681948800.0",
        )
        self.assertEqual(
            data["data"]["getAllIncomeStatements"][0]["period_end_date"], "1682121600.0"
        )
        self.assertEqual(data["data"]["getAllIncomeStatements"][0]["revenue"], 7500.00)
        self.assertEqual(
            data["data"]["getAllIncomeStatements"][0]["gross_profit"], 21500.00
        )
        self.assertEqual(
            data["data"]["getAllIncomeStatements"][0]["operating_expenses"], 4500.00
        )
        self.assertEqual(
            data["data"]["getAllIncomeStatements"][0]["net_income"], 17000.00
        )

    def test_get_income_statement(self):
        variables = {
            "account_id": self.account_id,
            "begin_date": "2023-04-20T15:30",
            "end_date": "2023-04-22T13:30",
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": generate_income_report, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        variables = {"uid": data["data"]["generateIncomeReport"]["uid"]}

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": get_income_statement, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            f"Something went wrong, {explain_status_code(response.status_code)}",
        )

        self.assertIsNotNone(data["data"]["getIncomeStatement"]["uid"])
        self.assertEqual(type(data["data"]["getIncomeStatement"]["uid"]), type(""))
        self.assertEqual(
            data["data"]["getIncomeStatement"]["account"]["id"], self.account_id
        )
        self.assertEqual(
            data["data"]["getIncomeStatement"]["period_start_date"], "1681948800.0"
        )
        self.assertEqual(
            data["data"]["getIncomeStatement"]["period_end_date"], "1682121600.0"
        )
        self.assertEqual(data["data"]["getIncomeStatement"]["revenue"], 7500.00)
        self.assertEqual(data["data"]["getIncomeStatement"]["gross_profit"], 21500.00)
        self.assertEqual(
            data["data"]["getIncomeStatement"]["operating_expenses"], 4500.00
        )
        self.assertEqual(data["data"]["getIncomeStatement"]["net_income"], 17000.00)

    def test_get_all_balance_sheet_statements(self):
        variables = {
            "account_id": self.account_id,
            "assets": [
                {"item": "Asset One", "net_worth": "1000.00"},
                {"item": "Asset Two", "net_worth": "2000.00"},
                {"item": "Asset Three", "net_worth": "3000.00"},
            ],
            "liabilities": [
                {"item": "Liability One", "net_worth": "100.00"},
                {"item": "Liability Two", "net_worth": "200.00"},
                {"item": "Liability Three", "net_worth": "300.00"},
            ],
            "equity": [
                {"item": "Capital Investment One", "net_worth": "100.00"},
                {"item": "Capital Investment Two", "net_worth": "200.00"},
            ],
        }

        response = self.client.post(
            "/graphql/",
            json.dumps(
                {"query": generate_balance_sheet_report, "variables": variables}
            ),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        variables = {"account_id": self.account_id}

        response = self.client.post(
            "/graphql/",
            json.dumps(
                {"query": get_all_balance_sheet_statements, "variables": variables}
            ),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            f"Something went wrong, {explain_status_code(response.status_code)}",
        )

        self.assertIsNotNone(data["data"]["getAllBalanceSheetStatements"][0]["uid"])
        self.assertEqual(
            type(data["data"]["getAllBalanceSheetStatements"][0]["uid"]), type("")
        )
        self.assertEqual(
            data["data"]["getAllBalanceSheetStatements"][0]["account"]["id"],
            self.account_id,
        )
        self.assertEqual(
            data["data"]["getAllBalanceSheetStatements"][0]["assets"], 29000.00
        )
        self.assertEqual(
            data["data"]["getAllBalanceSheetStatements"][0]["liabilities"], 600.00
        )
        self.assertEqual(
            data["data"]["getAllBalanceSheetStatements"][0]["equity"], 28700.00
        )

    def test_get_balance_sheet_statement(self):
        variables = {
            "account_id": self.account_id,
            "assets": [
                {"item": "Asset One", "net_worth": "1000.00"},
                {"item": "Asset Two", "net_worth": "2000.00"},
                {"item": "Asset Three", "net_worth": "3000.00"},
            ],
            "liabilities": [
                {"item": "Liability One", "net_worth": "100.00"},
                {"item": "Liability Two", "net_worth": "200.00"},
                {"item": "Liability Three", "net_worth": "300.00"},
            ],
            "equity": [
                {"item": "Capital Investment One", "net_worth": "100.00"},
                {"item": "Capital Investment Two", "net_worth": "200.00"},
            ],
        }

        response = self.client.post(
            "/graphql/",
            json.dumps(
                {"query": generate_balance_sheet_report, "variables": variables}
            ),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        variables = {"uid": data["data"]["generateBalanceSheetReport"]["uid"]}

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": get_balance_sheet_statement, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            f"Something went wrong, {explain_status_code(response.status_code)}",
        )

        self.assertIsNotNone(data["data"]["getBalanceSheetStatement"]["uid"])
        self.assertEqual(
            type(data["data"]["getBalanceSheetStatement"]["uid"]), type("")
        )
        self.assertEqual(
            data["data"]["getBalanceSheetStatement"]["account"]["id"], self.account_id
        )
        self.assertEqual(data["data"]["getBalanceSheetStatement"]["assets"], 29000.00)
        self.assertEqual(
            data["data"]["getBalanceSheetStatement"]["liabilities"], 600.00
        )
        self.assertEqual(data["data"]["getBalanceSheetStatement"]["equity"], 28700.00)
