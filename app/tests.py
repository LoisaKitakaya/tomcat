import json
from uuid import uuid4
from ariadne import gql
from django.test import TestCase, Client
from users.models import User, Profile, Plan
from app.models import (
    TransactionType,
    TransactionCategory,
    TransactionSubCategory,
    ProductCategory,
    ProductSubCategory,
)


def explain_status_code(status_code):
    status_codes = {
        200: "OK",
        201: "Created",
        204: "No Content",
        301: "Moved Permanently",
        302: "Moved Temporarily",
        304: "Not Modified",
        400: "Bad Request",
        401: "Unauthorized",
        403: "Forbidden",
        404: "Not Found",
        405: "Method Not Allowed",
        409: "Conflict",
        500: "Internal Server Error",
        501: "The server does not support the requested functionality",
        503: "Service Unavailable",
    }

    for key, value in status_codes.items():
        if status_code == key:
            return value


token_auth_mutation = gql(
    """
    mutation($username: String!, $password: String!) {
    tokenAuth(username: $username, password: $password) {
        payload
        token
        refresh_token
    }
    }
    """
)

create_test_user_mutation = gql(
    """
    mutation(
    $email: String!
    $first_name: String!
    $last_name: String!
    $workspace_name: String!
    $password: String!
    $password2: String!
    ) {
        createUser(
        email: $email
        first_name: $first_name
        last_name: $last_name
        workspace_name: $workspace_name
        password: $password
        password2: $password2
        ) {
            id
            email
            username
            first_name
            last_name
            is_staff
            is_active
        }
    }
    """
)

create_account_mutation = gql(
    """
    mutation(
        $account_name: String!
        $account_type: String!
        $account_balance: Float!
        $currency_code: String!
        ) {
        createAccount(
            account_name: $account_name
            account_type: $account_type
            account_balance: $account_balance
            currency_code: $currency_code
        ) {
            id
            account_name
            account_type
            owner {
                user {
                    username
                }
            }
            workspace {
                name
            }
            currency_code
            account_balance
        }
    }
    """
)

create_budget_mutation = gql(
    """
    mutation(
        $account_id: ID!
        $budget_name: String!
        $budget_description: String!
        $budget_amount: Float!
        $category: String!
        $sub_category: String!
        ) {
        createBudget(
            account_id: $account_id
            budget_name: $budget_name
            budget_description: $budget_description
            budget_amount: $budget_amount
            category: $category
            sub_category: $sub_category
        ) {
            id
            budget_name
            budget_description
            budget_amount
            budget_is_active
            owner {
                user {
                    username
                }
            }
            workspace {
                name
            }
            account {
                account_name
            }
            category {
                category_name
            }
            sub_category {
                category_name
            }
        }
    }
    """
)

create_target_mutation = gql(
    """
    mutation(
        $account_id: ID!
        $target_name: String!
        $target_description: String!
        $target_amount: Float!
        $category: String!
        $sub_category: String!
        ) {
        createTarget(
            account_id: $account_id
            target_name: $target_name
            target_description: $target_description
            target_amount: $target_amount
            category: $category
            sub_category: $sub_category
        ) {
            id
            target_name
            target_description
            target_amount
            target_is_active
            owner {
                user {
                    username
                }
            }
            workspace {
                name
            }
            account {
                account_name
            }
            category {
                category_name
            }
            sub_category {
                category_name
            }
        }
        }
    """
)

create_transaction_mutation = gql(
    """
    mutation(
        $account_id: ID!
        $transaction_type: String!
        $transaction_amount: Float!
        $transaction_date: String!
        $description: String!
        $category: String!
        $sub_category: String!
        ) {
        createTransaction(
            account_id: $account_id
            transaction_type: $transaction_type
            transaction_amount: $transaction_amount
            transaction_date: $transaction_date
            description: $description
            category: $category
            sub_category: $sub_category
        ) {
            id
            transaction_type
            transaction_amount
            currency_code
            description
            transaction_date
            account {
                account_balance
            }
            category {
                category_name
            }
            sub_category {
                category_name
            }
        }
    }
    """
)

create_employee_mutation = gql(
    """
    mutation(
        $account_id: ID!
        $email: String!
        $first_name: String!
        $last_name: String!
        $phone_number: String!
        $ID_number: String!
        $employment_status: String!
        $job_title: String!
        $job_description: String!
        $is_manager: Boolean!
        $salary: Float!
        $department: String!
        $employee_id: String!
        $emergency_contact_name: String!
        $emergency_contact_phone_number: String!
        $emergency_contact_email: String!
        $date_of_hire: String!
        ) {
        createEmployee(
            account_id: $account_id
            email: $email
            first_name: $first_name
            last_name: $last_name
            phone_number: $phone_number
            ID_number: $ID_number
            employment_status: $employment_status
            job_title: $job_title
            job_description: $job_description
            is_manager: $is_manager
            salary: $salary
            department: $department
            employee_id: $employee_id
            emergency_contact_name: $emergency_contact_name
            emergency_contact_phone_number: $emergency_contact_phone_number
            emergency_contact_email: $emergency_contact_email
            date_of_hire: $date_of_hire
        ) {
            id
            account {
                account_name
            }
            workspace {
                name
            }
            email
            first_name
            last_name
            phone_number
            ID_number
            employment_status
            job_title
            job_description
            is_manager
            salary
            department
            employee_id
            emergency_contact_name
            emergency_contact_phone_number
            emergency_contact_email
            date_of_hire
        }
    }
    """
)

create_product_mutation = gql(
    """
    mutation(
        $account_id: ID!
        $name: String!
        $description: String!
        $category: String!
        $sub_category: String!
        $buying_price: Float!
        $selling_price: Float!
        $current_stock_level: Int!
        $units_sold: Int!
        $reorder_level: Int!
        $supplier_name: String!
        $supplier_phone_number: String!
        $supplier_email: String!
        ) {
        createProduct(
            account_id: $account_id
            name: $name
            description: $description
            category: $category
            sub_category: $sub_category
            buying_price: $buying_price
            selling_price: $selling_price
            current_stock_level: $current_stock_level
            units_sold: $units_sold
            reorder_level: $reorder_level
            supplier_name: $supplier_name
            supplier_phone_number: $supplier_phone_number
            supplier_email: $supplier_email
        ) {
            id
            account {
                account_name
            }
            workspace {
                name
            }
            name
            description
            category {
                category_name
            }
            sub_category {
                category_name
            }
            buying_price
            selling_price
            current_stock_level
            units_sold
            reorder_level
            reorder_quantity
            supplier_name
            supplier_phone_number
            supplier_email
            profit_generated
        }
    }
    """
)


# Create your tests here.
class TestCustomDecorators(TestCase):
    def setUp(self) -> None:
        self.client = Client()

        self.standard_plan = Plan.objects.create(name="Standard")
        self.pro_plan = Plan.objects.create(name="Pro")

        self.test_user_one = User.objects.create(
            username="testuserone", email="testuserone@example.com"
        )
        self.test_user_one.set_password("#testpassword")
        self.test_user_one.save()

        self.user_one_workspace_uid = str(uuid4().hex)

        self.test_user_one_profile = Profile.objects.create(
            user=self.test_user_one,
            Plan=self.standard_plan,
            workspace_uid=self.user_one_workspace_uid,
        )

        self.test_user_two = User.objects.create(
            username="testusertwo", email="testusertwo@example.com"
        )
        self.test_user_two.set_password("#testpassword")
        self.test_user_two.save()

        self.user_two_workspace_uid = str(uuid4().hex)

        self.test_user_two_profile = Profile.objects.create(
            user=self.test_user_two,
            Plan=self.pro_plan,
            workspace_uid=self.user_two_workspace_uid,
        )

        user_one_token_auth_variables = {
            "username": self.test_user_one.username,
            "password": "#testpassword",
        }

        get_token = self.client.post(
            "/graphql/",
            json.dumps(
                {
                    "query": token_auth_mutation,
                    "variables": user_one_token_auth_variables,
                }
            ),
            content_type="application/json",
        )

        self.test_user_one_token = get_token.json()["data"]["tokenAuth"]["token"]

        user_two_token_auth_variables = {
            "username": self.test_user_two.username,
            "password": "#testpassword",
        }

        get_token = self.client.post(
            "/graphql/",
            json.dumps(
                {
                    "query": token_auth_mutation,
                    "variables": user_two_token_auth_variables,
                }
            ),
            content_type="application/json",
        )

        self.test_user_two_token = get_token.json()["data"]["tokenAuth"]["token"]

    def tearDown(self) -> None:
        self.client.logout()

        self.standard_plan.delete()
        self.pro_plan.delete()

        self.test_user_one.delete()
        self.test_user_two.delete()

        self.user_one_workspace_uid = None
        self.user_two_workspace_uid = None

        self.test_user_one_profile.delete()
        self.test_user_two_profile.delete()

        self.test_user_one_token = None
        self.test_user_two_token = None

    def test_check_plan_standard(self):
        query = gql(
            """
            query{
                testStandardDecorator{
                    name
                }
            }
            """
        )

        variables = {}

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": query, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.test_user_one_token}",
        )

        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            f"Something went wrong, {explain_status_code(response.status_code)}",
        )

        self.assertEqual(data["data"]["testStandardDecorator"]["name"], "Standard")

    def test_check_plan_pro(self):
        query = gql(
            """
            query{
                testStandardDecorator{
                    name
                }
            }
            """
        )

        variables = {}

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": query, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.test_user_two_token}",
        )

        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            f"Something went wrong, {explain_status_code(response.status_code)}",
        )

        self.assertEqual(data["data"]["testStandardDecorator"]["name"], "Pro")

    def test_check_if_employee(self):
        query = gql(
            """
            query{
                testIfIsEmployee
            }
            """
        )

        variables = {}

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": query, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.test_user_one_token}",
        )

        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            f"Something went wrong, {explain_status_code(response.status_code)}",
        )

        self.assertEqual(data["data"]["testIfIsEmployee"], True)


class TestAppMutations(TestCase):
    def setUp(self) -> None:
        self.client = Client()

        self.Plan = Plan.objects.create(name="Free")

        create_test_user_variables = {
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
                    "query": create_test_user_mutation,
                    "variables": create_test_user_variables,
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
            json.dumps(
                {"query": token_auth_mutation, "variables": token_auth_variables}
            ),
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

        self.product_category = ProductCategory.objects.create(
            category_name="Product category",
            category_description="Product category description",
        )
        self.product_subcategory = ProductSubCategory.objects.create(
            parent=self.product_category,
            category_name="Product subcategory",
            category_description="Product subcategory description",
        )

    def tearDown(self) -> None:
        self.client.logout()

        self.Plan.delete()

        self.test_username = None

        self.token = None

        self.transaction_category.delete()
        self.transaction_subcategory.delete()

        self.transaction_type_payable.delete()
        self.transaction_type_receivable.delete()

        self.product_category.delete()
        self.product_subcategory.delete()

    def test_create_account(self):
        variables = {
            "account_name": "KCB test account",
            "account_type": "Savings",
            "account_balance": 20000.00,
            "currency_code": "USD",
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": create_account_mutation, "variables": variables}),
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
        self.assertEqual(
            data["data"]["createAccount"]["owner"]["user"]["username"],
            "example@gmail.com",
        )
        self.assertEqual(
            data["data"]["createAccount"]["workspace"]["name"], "Important Workspace"
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
            json.dumps({"query": create_account_mutation, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            f"Something went wrong, {explain_status_code(response.status_code)}",
        )

        mutation = gql(
            """
            mutation(
            $id: ID!
            $account_name: String!
            $account_type: String!
            $account_balance: Float!
            $currency_code: String!
            ) {
                updateAccount(
                    id: $id
                    account_name: $account_name
                    account_type: $account_type
                    account_balance: $account_balance
                    currency_code: $currency_code
                ) {
                    account_name
                    account_type
                    owner {
                        user {
                            username
                        }
                    }
                    workspace {
                        name
                    }
                    currency_code
                    account_balance
                }
            }
            """
        )

        variables = {
            "id": data["data"]["createAccount"]["id"],
            "account_name": "Equity test account",
            "account_type": "Checking",
            "account_balance": 25000.00,
            "currency_code": "KES",
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": mutation, "variables": variables}),
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
        self.assertEqual(
            data["data"]["updateAccount"]["owner"]["user"]["username"],
            "example@gmail.com",
        )
        self.assertEqual(
            data["data"]["updateAccount"]["workspace"]["name"], "Important Workspace"
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
            json.dumps({"query": create_account_mutation, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            f"Something went wrong, {explain_status_code(response.status_code)}",
        )

        mutation = gql(
            """
            mutation($id: ID!) {
                deleteAccount(id: $id)
            }
            """
        )

        variables = {"id": data["data"]["createAccount"]["id"]}

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": mutation, "variables": variables}),
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

    def test_create_budget(self):
        variables = {
            "account_name": "KCB test account",
            "account_type": "Savings",
            "account_balance": 20000.00,
            "currency_code": "USD",
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": create_account_mutation, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            f"Something went wrong, {explain_status_code(response.status_code)}",
        )

        variables = {
            "account_id": data["data"]["createAccount"]["id"],
            "budget_name": "Test budget",
            "budget_description": "Test budget description",
            "budget_amount": 5000.00,
            "category": self.transaction_category.category_name,
            "sub_category": self.transaction_subcategory.category_name,
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": create_budget_mutation, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            f"Something went wrong, {explain_status_code(response.status_code)}",
        )

        self.assertEqual(data["data"]["createBudget"]["budget_name"], "Test budget")
        self.assertEqual(
            data["data"]["createBudget"]["budget_description"],
            "Test budget description",
        )
        self.assertEqual(data["data"]["createBudget"]["budget_amount"], 5000.00)
        self.assertEqual(data["data"]["createBudget"]["budget_is_active"], True)
        self.assertEqual(
            data["data"]["createBudget"]["category"]["category_name"], "Sales"
        )
        self.assertEqual(
            data["data"]["createBudget"]["sub_category"]["category_name"],
            "Product sales",
        )

    def test_update_budget(self):
        variables = {
            "account_name": "KCB test account",
            "account_type": "Savings",
            "account_balance": 20000.00,
            "currency_code": "USD",
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": create_account_mutation, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            f"Something went wrong, {explain_status_code(response.status_code)}",
        )

        variables = {
            "account_id": data["data"]["createAccount"]["id"],
            "budget_name": "Test budget",
            "budget_description": "Test budget description",
            "budget_amount": 5000.00,
            "category": self.transaction_category.category_name,
            "sub_category": self.transaction_subcategory.category_name,
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": create_budget_mutation, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            f"Something went wrong, {explain_status_code(response.status_code)}",
        )

        mutation = gql(
            """
            mutation(
                $id: ID!
                $budget_name: String!
                $budget_description: String!
                $budget_amount: Float!
                $category: String!
                $sub_category: String!
                ) {
                updateBudget(
                    id: $id
                    budget_name: $budget_name
                    budget_description: $budget_description
                    budget_amount: $budget_amount
                    category: $category
                    sub_category: $sub_category
                ) {
                    budget_name
                    budget_description
                    budget_amount
                    budget_is_active
                    owner {
                        user {
                            username
                        }
                    }
                    workspace {
                        name
                    }
                    account {
                        account_name
                    }
                    category {
                        category_name
                    }
                    sub_category {
                        category_name
                    }
                }
            }
            """
        )

        variables = {
            "id": data["data"]["createBudget"]["id"],
            "budget_name": "New budget",
            "budget_description": "New budget description",
            "budget_amount": 2500.00,
            "category": self.transaction_category.category_name,
            "sub_category": self.transaction_subcategory.category_name,
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": mutation, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            f"Something went wrong, {explain_status_code(response.status_code)}",
        )

        self.assertEqual(data["data"]["updateBudget"]["budget_name"], "New budget")
        self.assertEqual(
            data["data"]["updateBudget"]["budget_description"],
            "New budget description",
        )
        self.assertEqual(data["data"]["updateBudget"]["budget_amount"], 2500.00)

    def test_delete_budget(self):
        variables = {
            "account_name": "KCB test account",
            "account_type": "Savings",
            "account_balance": 20000.00,
            "currency_code": "USD",
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": create_account_mutation, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            f"Something went wrong, {explain_status_code(response.status_code)}",
        )

        variables = {
            "account_id": data["data"]["createAccount"]["id"],
            "budget_name": "Test budget",
            "budget_description": "Test budget description",
            "budget_amount": 5000.00,
            "category": self.transaction_category.category_name,
            "sub_category": self.transaction_subcategory.category_name,
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": create_budget_mutation, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            f"Something went wrong, {explain_status_code(response.status_code)}",
        )

        mutation = gql(
            """
            mutation($id: ID!) {
                deleteBudget(id: $id)
            }
            """
        )

        variables = {"id": data["data"]["createBudget"]["id"]}

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": mutation, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            f"Something went wrong, {explain_status_code(response.status_code)}",
        )

        self.assertEqual(data["data"]["deleteBudget"], True)

    def test_create_target(self):
        variables = {
            "account_name": "KCB test account",
            "account_type": "Savings",
            "account_balance": 20000.00,
            "currency_code": "USD",
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": create_account_mutation, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            f"Something went wrong, {explain_status_code(response.status_code)}",
        )

        variables = {
            "account_id": data["data"]["createAccount"]["id"],
            "target_name": "Test target",
            "target_description": "Test target description",
            "target_amount": 5000.00,
            "category": self.transaction_category.category_name,
            "sub_category": self.transaction_subcategory.category_name,
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": create_target_mutation, "variables": variables}),
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
            "account_name": "KCB test account",
            "account_type": "Savings",
            "account_balance": 20000.00,
            "currency_code": "USD",
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": create_account_mutation, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            f"Something went wrong, {explain_status_code(response.status_code)}",
        )

        variables = {
            "account_id": data["data"]["createAccount"]["id"],
            "target_name": "Test target",
            "target_description": "Test target description",
            "target_amount": 5000.00,
            "category": self.transaction_category.category_name,
            "sub_category": self.transaction_subcategory.category_name,
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": create_target_mutation, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            f"Something went wrong, {explain_status_code(response.status_code)}",
        )

        mutation = gql(
            """
            mutation(
                $id: ID!
                $target_name: String!
                $target_description: String!
                $target_amount: Float!
                $category: String!
                $sub_category: String!
                ) {
                updateTarget(
                    id: $id
                    target_name: $target_name
                    target_description: $target_description
                    target_amount: $target_amount
                    category: $category
                    sub_category: $sub_category
                ) {
                    target_name
                    target_description
                    target_amount
                    target_is_active
                    owner {
                        user {
                            username
                        }
                    }
                    workspace {
                        name
                    }
                    account {
                        account_name
                    }
                    category {
                        category_name
                    }
                    sub_category {
                        category_name
                    }
                }
            }
            """
        )

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
            json.dumps({"query": mutation, "variables": variables}),
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
            "account_name": "KCB test account",
            "account_type": "Savings",
            "account_balance": 20000.00,
            "currency_code": "USD",
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": create_account_mutation, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            f"Something went wrong, {explain_status_code(response.status_code)}",
        )

        variables = {
            "account_id": data["data"]["createAccount"]["id"],
            "target_name": "Test target",
            "target_description": "Test target description",
            "target_amount": 5000.00,
            "category": self.transaction_category.category_name,
            "sub_category": self.transaction_subcategory.category_name,
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": create_target_mutation, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            f"Something went wrong, {explain_status_code(response.status_code)}",
        )

        mutation = gql(
            """
            mutation($id: ID!) {
                deleteTarget(id: $id)
            }
            """
        )

        variables = {"id": data["data"]["createTarget"]["id"]}

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": mutation, "variables": variables}),
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

    def test_create_transaction(self):
        variables = {
            "account_name": "KCB test account",
            "account_type": "Savings",
            "account_balance": 20000.00,
            "currency_code": "USD",
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": create_account_mutation, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            f"Something went wrong, {explain_status_code(response.status_code)}",
        )

        variables = {
            "account_id": data["data"]["createAccount"]["id"],
            "transaction_type": self.transaction_type_receivable.type_name,
            "transaction_amount": 2500.00,
            "transaction_date": "2023-04-22T13:30",
            "description": "Test transaction description",
            "category": self.transaction_category.category_name,
            "sub_category": self.transaction_subcategory.category_name,
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": create_transaction_mutation, "variables": variables}),
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
            data["data"]["createTransaction"]["transaction_type"], "receivable"
        )
        self.assertEqual(
            data["data"]["createTransaction"]["transaction_amount"], 2500.00
        )
        self.assertEqual(
            data["data"]["createTransaction"]["transaction_date"], "1682159400.0"
        )
        self.assertEqual(
            data["data"]["createTransaction"]["account"]["account_balance"], 22500.00
        )

    def test_update_transaction(self):
        variables = {
            "account_name": "KCB test account",
            "account_type": "Savings",
            "account_balance": 20000.00,
            "currency_code": "USD",
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": create_account_mutation, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            f"Something went wrong, {explain_status_code(response.status_code)}",
        )

        account_id = data["data"]["createAccount"]["id"]

        variables = {
            "account_id": data["data"]["createAccount"]["id"],
            "transaction_type": self.transaction_type_receivable.type_name,
            "transaction_amount": 2500.00,
            "transaction_date": "2023-04-22T13:30",
            "description": "Test transaction description",
            "category": self.transaction_category.category_name,
            "sub_category": self.transaction_subcategory.category_name,
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": create_transaction_mutation, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            f"Something went wrong, {explain_status_code(response.status_code)}",
        )

        transaction_id = data["data"]["createTransaction"]["id"]

        mutation = gql(
            """
            mutation(
                $id: ID!
                $account_id: ID!
                $transaction_type: String!
                $transaction_amount: Float!
                $transaction_date: String!
                $description: String!
                $category: String!
                $sub_category: String!
                ) {
                updateTransaction(
                    id: $id
                    account_id: $account_id
                    transaction_type: $transaction_type
                    transaction_amount: $transaction_amount
                    transaction_date: $transaction_date
                    description: $description
                    category: $category
                    sub_category: $sub_category
                ) {
                    id
                    transaction_type
                    transaction_amount
                    currency_code
                    description
                    transaction_date
                    account {
                        account_balance
                    }
                    category {
                        category_name
                    }
                    sub_category {
                        category_name
                    }
                }
            }
            """
        )

        variables = {
            "id": transaction_id,
            "account_id": account_id,
            "transaction_type": self.transaction_type_payable.type_name,
            "transaction_amount": 3500.00,
            "transaction_date": "2023-03-20T15:30",
            "description": "Test transaction update",
            "category": self.transaction_category.category_name,
            "sub_category": self.transaction_subcategory.category_name,
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": mutation, "variables": variables}),
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
            data["data"]["updateTransaction"]["transaction_type"], "payable"
        )
        self.assertEqual(
            data["data"]["updateTransaction"]["transaction_amount"], 3500.00
        )
        self.assertEqual(
            data["data"]["updateTransaction"]["transaction_date"], "1679315400.0"
        )
        self.assertEqual(
            data["data"]["updateTransaction"]["account"]["account_balance"], 16500.00
        )

    def test_delete_transaction(self):
        variables = {
            "account_name": "KCB test account",
            "account_type": "Savings",
            "account_balance": 20000.00,
            "currency_code": "USD",
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": create_account_mutation, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            f"Something went wrong, {explain_status_code(response.status_code)}",
        )

        account_id = data["data"]["createAccount"]["id"]

        variables = {
            "account_id": data["data"]["createAccount"]["id"],
            "transaction_type": self.transaction_type_receivable.type_name,
            "transaction_amount": 2500.00,
            "transaction_date": "2023-04-22T13:30",
            "description": "Test transaction description",
            "category": self.transaction_category.category_name,
            "sub_category": self.transaction_subcategory.category_name,
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": create_transaction_mutation, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            f"Something went wrong, {explain_status_code(response.status_code)}",
        )

        transaction_id = data["data"]["createTransaction"]["id"]

        mutation = gql(
            """
            mutation($id: ID!, $account_id: ID!) {
                deleteTransaction(id: $id, account_id: $account_id)
            }
            """
        )

        variables = {"id": transaction_id, "account_id": account_id}

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": mutation, "variables": variables}),
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

    def test_create_employee(self):
        variables = {
            "account_name": "KCB test account",
            "account_type": "Savings",
            "account_balance": 20000.00,
            "currency_code": "USD",
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": create_account_mutation, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            f"Something went wrong, {explain_status_code(response.status_code)}",
        )

        variables = {
            "account_id": data["data"]["createAccount"]["id"],
            "email": "employee@example.com",
            "first_name": "New",
            "last_name": "Employee",
            "phone_number": "+254712345678",
            "ID_number": "123456789",
            "employment_status": "Contract",
            "job_title": "Consultant",
            "job_description": "Consulting ting",
            "is_manager": False,
            "salary": 3000.00,
            "department": "IT",
            "employee_id": "987654321",
            "emergency_contact_name": "Emergency Contact",
            "emergency_contact_phone_number": "+254787654321",
            "emergency_contact_email": "emergency@example.com",
            "date_of_hire": "2023-04-22",
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": create_employee_mutation, "variables": variables}),
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
            data["data"]["createEmployee"]["email"], "employee@example.com"
        )
        self.assertEqual(data["data"]["createEmployee"]["first_name"], "New")
        self.assertEqual(data["data"]["createEmployee"]["last_name"], "Employee")
        self.assertEqual(
            data["data"]["createEmployee"]["phone_number"], "+254712345678"
        )
        self.assertEqual(data["data"]["createEmployee"]["ID_number"], "123456789")
        self.assertEqual(
            data["data"]["createEmployee"]["employment_status"], "Contract"
        )
        self.assertEqual(data["data"]["createEmployee"]["job_title"], "Consultant")
        self.assertEqual(
            data["data"]["createEmployee"]["job_description"], "Consulting ting"
        )
        self.assertEqual(data["data"]["createEmployee"]["is_manager"], False)
        self.assertEqual(data["data"]["createEmployee"]["salary"], 3000.00)
        self.assertEqual(data["data"]["createEmployee"]["department"], "IT")
        self.assertEqual(data["data"]["createEmployee"]["employee_id"], "987654321")
        self.assertEqual(
            data["data"]["createEmployee"]["emergency_contact_name"],
            "Emergency Contact",
        )
        self.assertEqual(
            data["data"]["createEmployee"]["emergency_contact_phone_number"],
            "+254787654321",
        )
        self.assertEqual(
            data["data"]["createEmployee"]["emergency_contact_email"],
            "emergency@example.com",
        )
        self.assertEqual(data["data"]["createEmployee"]["date_of_hire"], "1682110800.0")

    def test_update_employee(self):
        variables = {
            "account_name": "KCB test account",
            "account_type": "Savings",
            "account_balance": 20000.00,
            "currency_code": "USD",
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": create_account_mutation, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            f"Something went wrong, {explain_status_code(response.status_code)}",
        )

        variables = {
            "account_id": data["data"]["createAccount"]["id"],
            "email": "employee@example.com",
            "first_name": "New",
            "last_name": "Employee",
            "phone_number": "+254712345678",
            "ID_number": "123456789",
            "employment_status": "Contract",
            "job_title": "Consultant",
            "job_description": "Consulting ting",
            "is_manager": False,
            "salary": 3000.00,
            "department": "IT",
            "employee_id": "987654321",
            "emergency_contact_name": "Emergency Contact",
            "emergency_contact_phone_number": "+254787654321",
            "emergency_contact_email": "emergency@example.com",
            "date_of_hire": "2023-04-22",
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": create_employee_mutation, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            f"Something went wrong, {explain_status_code(response.status_code)}",
        )

        mutation = gql(
            """
            mutation(
                $id: ID!
                $email: String!
                $first_name: String!
                $last_name: String!
                $phone_number: String!
                $ID_number: String!
                $employment_status: String!
                $job_title: String!
                $job_description: String!
                $is_manager: Boolean!
                $salary: Float!
                $department: String!
                $employee_id: String!
                $emergency_contact_name: String!
                $emergency_contact_phone_number: String!
                $emergency_contact_email: String!
                $date_of_hire: String!
                ) {
                updateEmployee(
                    id: $id
                    email: $email
                    first_name: $first_name
                    last_name: $last_name
                    phone_number: $phone_number
                    ID_number: $ID_number
                    employment_status: $employment_status
                    job_title: $job_title
                    job_description: $job_description
                    is_manager: $is_manager
                    salary: $salary
                    department: $department
                    employee_id: $employee_id
                    emergency_contact_name: $emergency_contact_name
                    emergency_contact_phone_number: $emergency_contact_phone_number
                    emergency_contact_email: $emergency_contact_email
                    date_of_hire: $date_of_hire
                ) {
                    account {
                        account_name
                    }
                    workspace {
                        name
                    }
                    email
                    first_name
                    last_name
                    phone_number
                    ID_number
                    employment_status
                    job_title
                    job_description
                    is_manager
                    salary
                    department
                    employee_id
                    emergency_contact_name
                    emergency_contact_phone_number
                    emergency_contact_email
                    date_of_hire
                }
            }
            """
        )

        variables = {
            "id": data["data"]["createEmployee"]["id"],
            "email": "",
            "first_name": "Old",
            "last_name": "",
            "phone_number": "+254787654321",
            "ID_number": "",
            "employment_status": "Full-time",
            "job_title": "Site Administrator",
            "job_description": "Administrating ting",
            "is_manager": True,
            "salary": 5000.00,
            "department": "",
            "employee_id": "2323232323",
            "emergency_contact_name": "",
            "emergency_contact_phone_number": "+254712345678",
            "emergency_contact_email": "",
            "date_of_hire": "2023-04-20",
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": mutation, "variables": variables}),
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
            data["data"]["updateEmployee"]["email"], "employee@example.com"
        )
        self.assertEqual(data["data"]["updateEmployee"]["first_name"], "Old")
        self.assertEqual(data["data"]["updateEmployee"]["last_name"], "Employee")
        self.assertEqual(
            data["data"]["updateEmployee"]["phone_number"], "+254787654321"
        )
        self.assertEqual(data["data"]["updateEmployee"]["ID_number"], "123456789")
        self.assertEqual(
            data["data"]["updateEmployee"]["employment_status"], "Full-time"
        )
        self.assertEqual(
            data["data"]["updateEmployee"]["job_title"], "Site Administrator"
        )
        self.assertEqual(
            data["data"]["updateEmployee"]["job_description"], "Administrating ting"
        )
        self.assertEqual(data["data"]["updateEmployee"]["is_manager"], True)
        self.assertEqual(data["data"]["updateEmployee"]["salary"], 5000.00)
        self.assertEqual(data["data"]["updateEmployee"]["department"], "IT")
        self.assertEqual(data["data"]["updateEmployee"]["employee_id"], "2323232323")
        self.assertEqual(
            data["data"]["updateEmployee"]["emergency_contact_name"],
            "Emergency Contact",
        )
        self.assertEqual(
            data["data"]["updateEmployee"]["emergency_contact_phone_number"],
            "+254712345678",
        )
        self.assertEqual(
            data["data"]["updateEmployee"]["emergency_contact_email"],
            "emergency@example.com",
        )
        self.assertEqual(data["data"]["updateEmployee"]["date_of_hire"], "1681938000.0")

    def test_delete_employee(self):
        variables = {
            "account_name": "KCB test account",
            "account_type": "Savings",
            "account_balance": 20000.00,
            "currency_code": "USD",
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": create_account_mutation, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            f"Something went wrong, {explain_status_code(response.status_code)}",
        )

        variables = {
            "account_id": data["data"]["createAccount"]["id"],
            "email": "employee@example.com",
            "first_name": "New",
            "last_name": "Employee",
            "phone_number": "+254712345678",
            "ID_number": "123456789",
            "employment_status": "Contract",
            "job_title": "Consultant",
            "job_description": "Consulting ting",
            "is_manager": False,
            "salary": 3000.00,
            "department": "IT",
            "employee_id": "987654321",
            "emergency_contact_name": "Emergency Contact",
            "emergency_contact_phone_number": "+254787654321",
            "emergency_contact_email": "emergency@example.com",
            "date_of_hire": "2023-04-22",
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": create_employee_mutation, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            f"Something went wrong, {explain_status_code(response.status_code)}",
        )

        mutation = gql(
            """
            mutation($id: ID!) {
                deleteEmployee(id: $id)
            }
            """
        )

        variables = {"id": data["data"]["createEmployee"]["id"]}

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": mutation, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            f"Something went wrong, {explain_status_code(response.status_code)}",
        )

        self.assertEqual(data["data"]["deleteEmployee"], True)

    def test_create_product(self):
        variables = {
            "account_name": "KCB test account",
            "account_type": "Savings",
            "account_balance": 20000.00,
            "currency_code": "USD",
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": create_account_mutation, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            f"Something went wrong, {explain_status_code(response.status_code)}",
        )

        variables = {
            "account_id": data["data"]["createAccount"]["id"],
            "name": "Product One",
            "description": "This is a test product",
            "category": self.product_category.category_name,
            "sub_category": self.product_subcategory.category_name,
            "buying_price": 300.00,
            "selling_price": 500.00,
            "current_stock_level": 100,
            "units_sold": 0,
            "reorder_level": 20,
            "supplier_name": "Supplier",
            "supplier_phone_number": "+254787654321",
            "supplier_email": "supplier@example.com",
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": create_product_mutation, "variables": variables}),
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
        self.assertEqual(data["data"]["createProduct"]["reorder_level"], 20)
        self.assertEqual(data["data"]["createProduct"]["reorder_quantity"], 0)
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
            "account_name": "KCB test account",
            "account_type": "Savings",
            "account_balance": 20000.00,
            "currency_code": "USD",
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": create_account_mutation, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            f"Something went wrong, {explain_status_code(response.status_code)}",
        )

        variables = {
            "account_id": data["data"]["createAccount"]["id"],
            "name": "Product One",
            "description": "This is a test product",
            "category": self.product_category.category_name,
            "sub_category": self.product_subcategory.category_name,
            "buying_price": 300.00,
            "selling_price": 500.00,
            "current_stock_level": 100,
            "units_sold": 0,
            "reorder_level": 20,
            "supplier_name": "Supplier",
            "supplier_phone_number": "+254787654321",
            "supplier_email": "supplier@example.com",
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": create_product_mutation, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            f"Something went wrong, {explain_status_code(response.status_code)}",
        )

        mutation = gql(
            """
            mutation(
                $id: ID!
                $name: String!
                $description: String!
                $category: String!
                $sub_category: String!
                $buying_price: Float!
                $selling_price: Float!
                $current_stock_level: Int!
                $units_sold: Int!
                $reorder_level: Int!
                $supplier_name: String!
                $supplier_phone_number: String!
                $supplier_email: String!
                ) {
                updateProduct(
                    id: $id
                    name: $name
                    description: $description
                    category: $category
                    sub_category: $sub_category
                    buying_price: $buying_price
                    selling_price: $selling_price
                    current_stock_level: $current_stock_level
                    units_sold: $units_sold
                    reorder_level: $reorder_level
                    supplier_name: $supplier_name
                    supplier_phone_number: $supplier_phone_number
                    supplier_email: $supplier_email
                ) {
                    account {
                        account_name
                    }
                    workspace {
                        name
                    }
                    name
                    description
                    category {
                        category_name
                    }
                    sub_category {
                        category_name
                    }
                    buying_price
                    selling_price
                    current_stock_level
                    units_sold
                    reorder_level
                    reorder_quantity
                    supplier_name
                    supplier_phone_number
                    supplier_email
                    profit_generated
                }
            }
            """
        )

        variables = {
            "id": data["data"]["createProduct"]["id"],
            "name": "Product One Update",
            "description": "",
            "category": self.product_category.category_name,
            "sub_category": self.product_subcategory.category_name,
            "buying_price": 350.00,
            "selling_price": 450.00,
            "current_stock_level": 100,
            "units_sold": 5,
            "reorder_level": 20,
            "supplier_name": "",
            "supplier_phone_number": "",
            "supplier_email": "supplierupdate@example.com",
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": mutation, "variables": variables}),
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
        self.assertEqual(data["data"]["updateProduct"]["current_stock_level"], 100)
        self.assertEqual(data["data"]["updateProduct"]["units_sold"], 5)
        self.assertEqual(data["data"]["updateProduct"]["reorder_level"], 20)
        self.assertEqual(data["data"]["updateProduct"]["reorder_quantity"], 5)
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
            "account_name": "KCB test account",
            "account_type": "Savings",
            "account_balance": 20000.00,
            "currency_code": "USD",
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": create_account_mutation, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            f"Something went wrong, {explain_status_code(response.status_code)}",
        )

        variables = {
            "account_id": data["data"]["createAccount"]["id"],
            "name": "Product One",
            "description": "This is a test product",
            "category": self.product_category.category_name,
            "sub_category": self.product_subcategory.category_name,
            "buying_price": 300.00,
            "selling_price": 500.00,
            "current_stock_level": 100,
            "units_sold": 0,
            "reorder_level": 20,
            "supplier_name": "Supplier",
            "supplier_phone_number": "+254787654321",
            "supplier_email": "supplier@example.com",
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": create_product_mutation, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            f"Something went wrong, {explain_status_code(response.status_code)}",
        )

        mutation = gql(
            """
            mutation($id: ID!) {
                deleteProduct(id: $id)
            }
            """
        )

        variables = {"id": data["data"]["createProduct"]["id"]}

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": mutation, "variables": variables}),
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

        self.Plan = Plan.objects.create(name="Free")

        create_test_user_variables = {
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
                    "query": create_test_user_mutation,
                    "variables": create_test_user_variables,
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
            json.dumps(
                {"query": token_auth_mutation, "variables": token_auth_variables}
            ),
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
            "account_balance": 20000.00,
            "currency_code": "USD",
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": create_account_mutation, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            f"Something went wrong, {explain_status_code(response.status_code)}",
        )

        self.account_id = data["data"]["createAccount"]["id"]

        variables = {
            "account_id": self.account_id,
            "budget_name": "Test budget",
            "budget_description": "Test budget description",
            "budget_amount": 5000.00,
            "category": self.transaction_category.category_name,
            "sub_category": self.transaction_subcategory.category_name,
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": create_budget_mutation, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            f"Something went wrong, {explain_status_code(response.status_code)}",
        )

        self.budget_id = data["data"]["createBudget"]["id"]

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
            json.dumps({"query": create_target_mutation, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            f"Something went wrong, {explain_status_code(response.status_code)}",
        )

        self.target_id = data["data"]["createTarget"]["id"]

        variables = {
            "account_id": self.account_id,
            "transaction_type": self.transaction_type_receivable.type_name,
            "transaction_amount": 2500.00,
            "transaction_date": "2023-04-22T13:30",
            "description": "Test transaction description",
            "category": self.transaction_category.category_name,
            "sub_category": self.transaction_subcategory.category_name,
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": create_transaction_mutation, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            f"Something went wrong, {explain_status_code(response.status_code)}",
        )

        self.transaction_id = data["data"]["createTransaction"]["id"]

        variables = {
            "account_id": self.account_id,
            "email": "employee@example.com",
            "first_name": "New",
            "last_name": "Employee",
            "phone_number": "+254712345678",
            "ID_number": "123456789",
            "employment_status": "Contract",
            "job_title": "Consultant",
            "job_description": "Consulting ting",
            "is_manager": False,
            "salary": 3000.00,
            "department": "IT",
            "employee_id": "987654321",
            "emergency_contact_name": "Emergency Contact",
            "emergency_contact_phone_number": "+254787654321",
            "emergency_contact_email": "emergency@example.com",
            "date_of_hire": "2023-04-22",
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": create_employee_mutation, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            f"Something went wrong, {explain_status_code(response.status_code)}",
        )

        self.employee_id = data["data"]["createEmployee"]["id"]

        variables = {
            "account_id": self.account_id,
            "name": "Product One",
            "description": "This is a test product",
            "category": self.product_category.category_name,
            "sub_category": self.product_subcategory.category_name,
            "buying_price": 300.00,
            "selling_price": 500.00,
            "current_stock_level": 100,
            "units_sold": 0,
            "reorder_level": 20,
            "supplier_name": "Supplier",
            "supplier_phone_number": "+254787654321",
            "supplier_email": "supplier@example.com",
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": create_product_mutation, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            f"Something went wrong, {explain_status_code(response.status_code)}",
        )

        self.product_id = data["data"]["createProduct"]["id"]

    def tearDown(self) -> None:
        self.client.logout()

        self.Plan.delete()

        self.test_username = None

        self.token = None

        self.transaction_category.delete()
        self.transaction_subcategory.delete()

        self.transaction_type_payable.delete()
        self.transaction_type_receivable.delete()

        self.product_category.delete()
        self.product_subcategory.delete()

        self.account_id = None

        self.budget_id = None

        self.target_id = None

        self.transaction_id = None

        self.employee_id = None

        self.product_id = None

    def test_get_all_accounts(self):
        query = gql(
            """
            query {
                getAllAccounts {
                    account_name
                    account_type
                    owner {
                        user {
                            username
                        }
                    }
                    workspace {
                        name
                    }
                    currency_code
                    account_balance
                }
            }
            """
        )

        variables = {}

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": query, "variables": variables}),
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
        self.assertEqual(data["data"]["getAllAccounts"][0]["account_balance"], 22500.00)
        self.assertEqual(data["data"]["getAllAccounts"][0]["currency_code"], "USD")
        self.assertEqual(
            data["data"]["getAllAccounts"][0]["account_name"], "KCB test account"
        )
        self.assertEqual(
            data["data"]["getAllAccounts"][0]["owner"]["user"]["username"],
            "example@gmail.com",
        )
        self.assertEqual(
            data["data"]["getAllAccounts"][0]["workspace"]["name"],
            "Important Workspace",
        )

    def test_get_account(self):
        query = gql(
            """
            query($id: ID!) {
                getAccount(id: $id) {
                    account_name
                    account_type
                    owner {
                        user {
                            username
                        }
                    }
                    workspace {
                        name
                    }
                    currency_code
                    account_balance
                }
            }
            """
        )

        variables = {"id": self.account_id}

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": query, "variables": variables}),
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
        self.assertEqual(data["data"]["getAccount"]["account_balance"], 22500.00)
        self.assertEqual(data["data"]["getAccount"]["currency_code"], "USD")
        self.assertEqual(data["data"]["getAccount"]["account_name"], "KCB test account")
        self.assertEqual(
            data["data"]["getAccount"]["owner"]["user"]["username"],
            "example@gmail.com",
        )
        self.assertEqual(
            data["data"]["getAccount"]["workspace"]["name"], "Important Workspace"
        )

    def test_get_all_budgets(self):
        query = gql(
            """
            query {
                getAllBudgets {
                    budget_name
                    budget_description
                    budget_is_active
                    budget_amount
                    owner {
                        user {
                            username
                        }
                    }
                    workspace {
                        name
                    }
                    account {
                        account_name
                    }
                    category {
                        category_name
                    }
                    sub_category {
                        category_name
                    }
                }
            }
            """
        )

        variables = {}

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": query, "variables": variables}),
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
            response.status_code,
            200,
            f"Something went wrong, {explain_status_code(response.status_code)}",
        )

        self.assertEqual(data["data"]["getAllBudgets"][0]["budget_name"], "Test budget")
        self.assertEqual(
            data["data"]["getAllBudgets"][0]["budget_description"],
            "Test budget description",
        )
        self.assertEqual(data["data"]["getAllBudgets"][0]["budget_amount"], 5000.00)
        self.assertEqual(data["data"]["getAllBudgets"][0]["budget_is_active"], True)
        self.assertEqual(
            data["data"]["getAllBudgets"][0]["category"]["category_name"], "Sales"
        )
        self.assertEqual(
            data["data"]["getAllBudgets"][0]["sub_category"]["category_name"],
            "Product sales",
        )

    def test_get_budget(self):
        query = gql(
            """
            query($id: ID!) {
                getBudget(id: $id) {
                    budget_name
                    budget_description
                    budget_is_active
                    budget_amount
                    owner {
                        user {
                            username
                        }
                    }
                    workspace {
                        name
                    }
                    account {
                        account_name
                    }
                    category {
                        category_name
                    }
                    sub_category {
                        category_name
                    }
                }
            }
            """
        )

        variables = {"id": self.budget_id}

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": query, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            f"Something went wrong, {explain_status_code(response.status_code)}",
        )

        self.assertEqual(data["data"]["getBudget"]["budget_name"], "Test budget")
        self.assertEqual(
            data["data"]["getBudget"]["budget_description"],
            "Test budget description",
        )
        self.assertEqual(data["data"]["getBudget"]["budget_amount"], 5000.00)
        self.assertEqual(data["data"]["getBudget"]["budget_is_active"], True)
        self.assertEqual(
            data["data"]["getBudget"]["category"]["category_name"], "Sales"
        )
        self.assertEqual(
            data["data"]["getBudget"]["sub_category"]["category_name"],
            "Product sales",
        )

    def test_get_all_targets(self):
        query = gql(
            """
            query {
                getAllTargets {
                    target_name
                    target_description
                    target_is_active
                    target_amount
                    owner {
                        user {
                            username
                        }
                    }
                    workspace {
                        name
                    }
                    account {
                        account_name
                    }
                    category {
                        category_name
                    }
                    sub_category {
                        category_name
                    }
                }
            }
            """
        )

        variables = {}

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": query, "variables": variables}),
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
        query = gql(
            """
            query($id: ID!) {
                getTarget(id: $id) {
                    target_name
                    target_description
                    target_is_active
                    target_amount
                    owner {
                        user {
                            username
                        }
                    }
                    workspace {
                        name
                    }
                    account {
                        account_name
                    }
                    category {
                        category_name
                    }
                    sub_category {
                        category_name
                    }
                }
            }
            """
        )

        variables = {"id": self.target_id}

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": query, "variables": variables}),
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

    def test_get_all_transactions(self):
        query = gql(
            """
            query($id: ID!) {
                getAllTransactions(id: $id) {
                    transaction_type
                    transaction_amount
                    currency_code
                    description
                    transaction_date
                    account {
                        account_balance
                    }
                    category {
                        category_name
                    }
                    sub_category {
                        category_name
                    }
                }
            }
            """
        )

        variables = {"id": self.account_id}

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": query, "variables": variables}),
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
            data["data"]["getAllTransactions"][0]["transaction_type"], "receivable"
        )
        self.assertEqual(
            data["data"]["getAllTransactions"][0]["transaction_amount"], 2500.00
        )
        self.assertEqual(
            data["data"]["getAllTransactions"][0]["transaction_date"], "1682148600.0"
        )
        self.assertEqual(
            data["data"]["getAllTransactions"][0]["account"]["account_balance"],
            22500.00,
        )

    def test_get_transaction(self):
        query = gql(
            """
            query($id: ID!) {
                getTransaction(id: $id) {
                    transaction_type
                    transaction_amount
                    currency_code
                    description
                    transaction_date
                    account {
                        account_balance
                    }
                    category {
                        category_name
                    }
                    sub_category {
                        category_name
                    }
                }
            }
            """
        )

        variables = {"id": self.transaction_id}

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": query, "variables": variables}),
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
            data["data"]["getTransaction"]["transaction_type"], "receivable"
        )
        self.assertEqual(data["data"]["getTransaction"]["transaction_amount"], 2500.00)
        self.assertEqual(
            data["data"]["getTransaction"]["transaction_date"], "1682148600.0"
        )
        self.assertEqual(
            data["data"]["getTransaction"]["account"]["account_balance"],
            22500.00,
        )

    def test_get_all_employees(self):
        query = gql(
            """
            query($account_id: ID!) {
                getAllEmployees(account_id: $account_id) {
                    account {
                        account_name
                    }
                    workspace {
                        name
                    }
                    email
                    first_name
                    last_name
                    phone_number
                    ID_number
                    employment_status
                    job_title
                    job_description
                    is_manager
                    salary
                    department
                    employee_id
                    emergency_contact_name
                    emergency_contact_phone_number
                    emergency_contact_email
                    date_of_hire
                }
            }
            """
        )

        variables = {"account_id": self.account_id}

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": query, "variables": variables}),
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
            data["data"]["getAllEmployees"][0]["email"], "employee@example.com"
        )
        self.assertEqual(data["data"]["getAllEmployees"][0]["first_name"], "New")
        self.assertEqual(data["data"]["getAllEmployees"][0]["last_name"], "Employee")
        self.assertEqual(
            data["data"]["getAllEmployees"][0]["phone_number"], "+254712345678"
        )
        self.assertEqual(data["data"]["getAllEmployees"][0]["ID_number"], "123456789")
        self.assertEqual(
            data["data"]["getAllEmployees"][0]["employment_status"], "Contract"
        )
        self.assertEqual(data["data"]["getAllEmployees"][0]["job_title"], "Consultant")
        self.assertEqual(
            data["data"]["getAllEmployees"][0]["job_description"], "Consulting ting"
        )
        self.assertEqual(data["data"]["getAllEmployees"][0]["is_manager"], False)
        self.assertEqual(data["data"]["getAllEmployees"][0]["salary"], 3000.00)
        self.assertEqual(data["data"]["getAllEmployees"][0]["department"], "IT")
        self.assertEqual(data["data"]["getAllEmployees"][0]["employee_id"], "987654321")
        self.assertEqual(
            data["data"]["getAllEmployees"][0]["emergency_contact_name"],
            "Emergency Contact",
        )
        self.assertEqual(
            data["data"]["getAllEmployees"][0]["emergency_contact_phone_number"],
            "+254787654321",
        )
        self.assertEqual(
            data["data"]["getAllEmployees"][0]["emergency_contact_email"],
            "emergency@example.com",
        )
        self.assertEqual(data["data"]["getAllEmployees"][0]["date_of_hire"], "1682110800.0")

    def test_get_employee(self):
        query = gql(
            """
            query($id: ID!) {
                getEmployee(id: $id) {
                    account {
                        account_name
                    }
                    workspace {
                        name
                    }
                    email
                    first_name
                    last_name
                    phone_number
                    ID_number
                    employment_status
                    job_title
                    job_description
                    is_manager
                    salary
                    department
                    employee_id
                    emergency_contact_name
                    emergency_contact_phone_number
                    emergency_contact_email
                    date_of_hire
                }
            }
            """
        )

        variables = {"id": self.employee_id}

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": query, "variables": variables}),
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
            data["data"]["getEmployee"]["email"], "employee@example.com"
        )
        self.assertEqual(data["data"]["getEmployee"]["first_name"], "New")
        self.assertEqual(data["data"]["getEmployee"]["last_name"], "Employee")
        self.assertEqual(
            data["data"]["getEmployee"]["phone_number"], "+254712345678"
        )
        self.assertEqual(data["data"]["getEmployee"]["ID_number"], "123456789")
        self.assertEqual(
            data["data"]["getEmployee"]["employment_status"], "Contract"
        )
        self.assertEqual(data["data"]["getEmployee"]["job_title"], "Consultant")
        self.assertEqual(
            data["data"]["getEmployee"]["job_description"], "Consulting ting"
        )
        self.assertEqual(data["data"]["getEmployee"]["is_manager"], False)
        self.assertEqual(data["data"]["getEmployee"]["salary"], 3000.00)
        self.assertEqual(data["data"]["getEmployee"]["department"], "IT")
        self.assertEqual(data["data"]["getEmployee"]["employee_id"], "987654321")
        self.assertEqual(
            data["data"]["getEmployee"]["emergency_contact_name"],
            "Emergency Contact",
        )
        self.assertEqual(
            data["data"]["getEmployee"]["emergency_contact_phone_number"],
            "+254787654321",
        )
        self.assertEqual(
            data["data"]["getEmployee"]["emergency_contact_email"],
            "emergency@example.com",
        )
        self.assertEqual(data["data"]["getEmployee"]["date_of_hire"], "1682110800.0")

    def test_get_all_products(self):
        query = gql(
            """
            query($account_id: ID!) {
                getAllProducts(account_id: $account_id) {
                    account {
                        account_name
                    }
                    workspace {
                        name
                    }
                    name
                    description
                    category {
                        category_name
                    }
                    sub_category {
                        category_name
                    }
                    buying_price
                    selling_price
                    current_stock_level
                    units_sold
                    reorder_level
                    reorder_quantity
                    supplier_name
                    supplier_phone_number
                    supplier_email
                    profit_generated
                }
            }
            """
        )

        variables = {"account_id": self.account_id}

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": query, "variables": variables}),
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
        self.assertEqual(data["data"]["getAllProducts"][0]["reorder_level"], 20)
        self.assertEqual(data["data"]["getAllProducts"][0]["reorder_quantity"], 0)
        self.assertEqual(data["data"]["getAllProducts"][0]["profit_generated"], 0)
        self.assertEqual(data["data"]["getAllProducts"][0]["supplier_name"], "Supplier")
        self.assertEqual(
            data["data"]["getAllProducts"][0]["supplier_phone_number"], "+254787654321"
        )
        self.assertEqual(
            data["data"]["getAllProducts"][0]["supplier_email"], "supplier@example.com"
        )

    def test_get_product(self):
        query = gql(
            """
            query($id: ID!) {
                getProduct(id: $id) {
                    account {
                        account_name
                    }
                    workspace {
                        name
                    }
                    name
                    description
                    category {
                        category_name
                    }
                    sub_category {
                        category_name
                    }
                    buying_price
                    selling_price
                    current_stock_level
                    units_sold
                    reorder_level
                    reorder_quantity
                    supplier_name
                    supplier_phone_number
                    supplier_email
                    profit_generated
                }
            }
            """
        )

        variables = {"id": self.product_id}

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": query, "variables": variables}),
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
        self.assertEqual(data["data"]["getProduct"]["reorder_level"], 20)
        self.assertEqual(data["data"]["getProduct"]["reorder_quantity"], 0)
        self.assertEqual(data["data"]["getProduct"]["profit_generated"], 0)
        self.assertEqual(data["data"]["getProduct"]["supplier_name"], "Supplier")
        self.assertEqual(
            data["data"]["getProduct"]["supplier_phone_number"], "+254787654321"
        )
        self.assertEqual(
            data["data"]["getProduct"]["supplier_email"], "supplier@example.com"
        )
