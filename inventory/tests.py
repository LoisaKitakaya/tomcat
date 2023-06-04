import json
from plans.models import Plan
from django.test import TestCase, Client
from controls.test_ref import explain_status_code
from inventory.models import ProductCategory, ProductSubCategory

from controls.mutation_ref import (
    token_auth,
    create_user,
    create_account,
    create_product,
    update_product,
    delete_product,
)
from controls.query_ref import get_all_products, get_product


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
            category_name="Product category",
            category_description="Product category description",
        )
        self.product_subcategory = ProductSubCategory.objects.create(
            parent=self.product_category,
            category_name="Product subcategory",
            category_description="Product subcategory description",
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

        self.product_category.delete()

        self.product_subcategory.delete()

    def test_create_product(self):
        variables = {
            "account_id": self.account_id,
            "name": "Product One",
            "description": "This is a test product",
            "category": self.product_category.category_name,
            "sub_category": self.product_subcategory.category_name,
            "buying_price": "300.00",
            "selling_price": "500.00",
            "current_stock_level": "100",
            "units_sold": "0",
            "supplier_name": "Supplier",
            "supplier_phone_number": "+254787654321",
            "supplier_email": "supplier@example.com",
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": create_product, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            f"Something went wrong, {explain_status_code(response.status_code)}",
        )

        self.assertEqual(data["data"]["createProduct"]["name"], "Product One")
        self.assertEqual(
            data["data"]["createProduct"]["category"]["category_name"],
            "Product category",
        )
        self.assertEqual(
            data["data"]["createProduct"]["sub_category"]["category_name"],
            "Product subcategory",
        )
        self.assertEqual(data["data"]["createProduct"]["buying_price"], 300.00)
        self.assertEqual(data["data"]["createProduct"]["selling_price"], 500.00)
        self.assertEqual(data["data"]["createProduct"]["current_stock_level"], 100)
        self.assertEqual(data["data"]["createProduct"]["units_sold"], 0)
        self.assertEqual(data["data"]["createProduct"]["profit_generated"], 0)
        self.assertEqual(data["data"]["createProduct"]["supplier_name"], "Supplier")
        self.assertEqual(
            data["data"]["createProduct"]["supplier_phone_number"], "+254787654321"
        )
        self.assertEqual(
            data["data"]["createProduct"]["supplier_email"], "supplier@example.com"
        )

    def test_update_product(self):
        variables = {
            "account_id": self.account_id,
            "name": "Product One",
            "description": "This is a test product",
            "category": self.product_category.category_name,
            "sub_category": self.product_subcategory.category_name,
            "buying_price": "300.00",
            "selling_price": "500.00",
            "current_stock_level": "100",
            "units_sold": "0",
            "supplier_name": "Supplier",
            "supplier_phone_number": "+254787654321",
            "supplier_email": "supplier@example.com",
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": create_product, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        variables = {
            "id": data["data"]["createProduct"]["id"],
            "name": "Product One Update",
            "description": "",
            "category": self.product_category.category_name,
            "sub_category": self.product_subcategory.category_name,
            "buying_price": "350.00",
            "selling_price": "450.00",
            "current_stock_level": "",
            "units_sold": "5",
            "supplier_name": "",
            "supplier_phone_number": "",
            "supplier_email": "supplierupdate@example.com",
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": update_product, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            f"Something went wrong, {explain_status_code(response.status_code)}",
        )

        self.assertEqual(data["data"]["updateProduct"]["name"], "Product One Update")
        self.assertEqual(
            data["data"]["updateProduct"]["category"]["category_name"],
            "Product category",
        )
        self.assertEqual(
            data["data"]["updateProduct"]["sub_category"]["category_name"],
            "Product subcategory",
        )
        self.assertEqual(data["data"]["updateProduct"]["buying_price"], 350.00)
        self.assertEqual(data["data"]["updateProduct"]["selling_price"], 450.00)
        self.assertEqual(data["data"]["updateProduct"]["current_stock_level"], 95)
        self.assertEqual(data["data"]["updateProduct"]["units_sold"], 5)
        self.assertEqual(data["data"]["updateProduct"]["profit_generated"], 500)
        self.assertEqual(data["data"]["updateProduct"]["supplier_name"], "Supplier")
        self.assertEqual(
            data["data"]["updateProduct"]["supplier_phone_number"], "+254787654321"
        )
        self.assertEqual(
            data["data"]["updateProduct"]["supplier_email"],
            "supplierupdate@example.com",
        )

    def test_delete_product(self):
        variables = {
            "account_id": self.account_id,
            "name": "Product One",
            "description": "This is a test product",
            "category": self.product_category.category_name,
            "sub_category": self.product_subcategory.category_name,
            "buying_price": "300.00",
            "selling_price": "500.00",
            "current_stock_level": "100",
            "units_sold": "0",
            "supplier_name": "Supplier",
            "supplier_phone_number": "+254787654321",
            "supplier_email": "supplier@example.com",
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": create_product, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        variables = {"id": data["data"]["createProduct"]["id"]}

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": delete_product, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            f"Something went wrong, {explain_status_code(response.status_code)}",
        )

        self.assertEqual(data["data"]["deleteProduct"], True)


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
            category_name="Product category",
            category_description="Product category description",
        )
        self.product_subcategory = ProductSubCategory.objects.create(
            parent=self.product_category,
            category_name="Product subcategory",
            category_description="Product subcategory description",
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
            "name": "Product One",
            "description": "This is a test product",
            "category": self.product_category.category_name,
            "sub_category": self.product_subcategory.category_name,
            "buying_price": "300.00",
            "selling_price": "500.00",
            "current_stock_level": "100",
            "units_sold": "0",
            "supplier_name": "Supplier",
            "supplier_phone_number": "+254787654321",
            "supplier_email": "supplier@example.com",
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": create_product, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        self.product_id = data["data"]["createProduct"]["id"]

    def tearDown(self):
        self.client.logout()

        self.plan.delete()

        self.test_username = None

        self.token = None

        self.account_id = None

        self.product_category.delete()

        self.product_subcategory.delete()

        self.product_id = None

    def test_get_all_products(self):
        variables = {"account_id": self.account_id}

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": get_all_products, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            f"Something went wrong, {explain_status_code(response.status_code)}",
        )

        self.assertEqual(data["data"]["getAllProducts"][0]["name"], "Product One")
        self.assertEqual(
            data["data"]["getAllProducts"][0]["category"]["category_name"],
            "Product category",
        )
        self.assertEqual(
            data["data"]["getAllProducts"][0]["sub_category"]["category_name"],
            "Product subcategory",
        )
        self.assertEqual(data["data"]["getAllProducts"][0]["buying_price"], 300.00)
        self.assertEqual(data["data"]["getAllProducts"][0]["selling_price"], 500.00)
        self.assertEqual(data["data"]["getAllProducts"][0]["current_stock_level"], 100)
        self.assertEqual(data["data"]["getAllProducts"][0]["units_sold"], 0)
        self.assertEqual(data["data"]["getAllProducts"][0]["profit_generated"], 0)
        self.assertEqual(data["data"]["getAllProducts"][0]["supplier_name"], "Supplier")
        self.assertEqual(
            data["data"]["getAllProducts"][0]["supplier_phone_number"], "+254787654321"
        )
        self.assertEqual(
            data["data"]["getAllProducts"][0]["supplier_email"], "supplier@example.com"
        )

    def test_get_product(self):
        variables = {"id": self.product_id}

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": get_product, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            f"Something went wrong, {explain_status_code(response.status_code)}",
        )

        self.assertEqual(data["data"]["getProduct"]["name"], "Product One")
        self.assertEqual(
            data["data"]["getProduct"]["category"]["category_name"],
            "Product category",
        )
        self.assertEqual(
            data["data"]["getProduct"]["sub_category"]["category_name"],
            "Product subcategory",
        )
        self.assertEqual(data["data"]["getProduct"]["buying_price"], 300.00)
        self.assertEqual(data["data"]["getProduct"]["selling_price"], 500.00)
        self.assertEqual(data["data"]["getProduct"]["current_stock_level"], 100)
        self.assertEqual(data["data"]["getProduct"]["units_sold"], 0)
        self.assertEqual(data["data"]["getProduct"]["profit_generated"], 0)
        self.assertEqual(data["data"]["getProduct"]["supplier_name"], "Supplier")
        self.assertEqual(
            data["data"]["getProduct"]["supplier_phone_number"], "+254787654321"
        )
        self.assertEqual(
            data["data"]["getProduct"]["supplier_email"], "supplier@example.com"
        )
