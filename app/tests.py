import json
from uuid import uuid4
from ariadne import gql
from django.test import TestCase, Client
from users.models import User, Profile, Package
from app.models import TransactionType, TransactionCategory, TransactionSubCategory


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


# Create your tests here.
class TestCustomDecorators(TestCase):
    def setUp(self) -> None:
        self.client = Client()

        self.standard_package = Package.objects.create(name="Standard")
        self.pro_package = Package.objects.create(name="Pro")

        self.test_user_one = User.objects.create(
            username="testuserone", email="testuserone@example.com"
        )
        self.test_user_one.set_password("#testpassword")
        self.test_user_one.save()

        self.user_one_workspace_uid = str(uuid4().hex)

        self.test_user_one_profile = Profile.objects.create(
            user=self.test_user_one,
            package=self.standard_package,
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
            package=self.pro_package,
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

        self.test_user_one_token = get_token.json()[
            "data"]["tokenAuth"]["token"]

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

        self.test_user_two_token = get_token.json()[
            "data"]["tokenAuth"]["token"]

    def tearDown(self) -> None:
        self.client.logout()

        self.standard_package.delete()
        self.pro_package.delete()

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

        self.assertEqual(
            data["data"]["testStandardDecorator"]["name"], "Standard")

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


class TestAppMutations(TestCase):
    def setUp(self) -> None:
        self.client = Client()

        self.package = Package.objects.create(name="Free")

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

    def tearDown(self) -> None:
        self.client.logout()

        self.package.delete()

        self.test_username = None

        self.token = None

        self.transaction_category.delete()

        self.transaction_subcategory.delete()

        self.transaction_type_payable.delete()
        self.transaction_type_receivable.delete()

    def test_create_account(self):
        variables = {
            "account_name": "KCB test account",
            "account_type": "Savings",
            "account_balance": 20000.00,
            "currency_code": "USD",
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": create_account_mutation,
                       "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            f"Something went wrong, {explain_status_code(response.status_code)}",
        )

        self.assertEqual(data["data"]["createAccount"]
                         ["account_type"], "Savings")
        self.assertEqual(data["data"]["createAccount"]
                         ["account_balance"], 20000.00)
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
            json.dumps({"query": create_account_mutation,
                       "variables": variables}),
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

        self.assertEqual(data["data"]["updateAccount"]
                         ["account_type"], "Checking")
        self.assertEqual(data["data"]["updateAccount"]
                         ["account_balance"], 25000.00)
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
            json.dumps({"query": create_account_mutation,
                       "variables": variables}),
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
            json.dumps({"query": create_account_mutation,
                       "variables": variables}),
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
            json.dumps({"query": create_budget_mutation,
                       "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            f"Something went wrong, {explain_status_code(response.status_code)}",
        )

        self.assertEqual(data["data"]["createBudget"]
                         ["budget_name"], "Test budget")
        self.assertEqual(
            data["data"]["createBudget"]["budget_description"],
            "Test budget description",
        )
        self.assertEqual(data["data"]["createBudget"]
                         ["budget_amount"], 5000.00)
        self.assertEqual(data["data"]["createBudget"]
                         ["budget_is_active"], True)
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
            json.dumps({"query": create_account_mutation,
                       "variables": variables}),
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
            json.dumps({"query": create_budget_mutation,
                       "variables": variables}),
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

        self.assertEqual(data["data"]["updateBudget"]
                         ["budget_name"], "New budget")
        self.assertEqual(
            data["data"]["updateBudget"]["budget_description"],
            "New budget description",
        )
        self.assertEqual(data["data"]["updateBudget"]
                         ["budget_amount"], 2500.00)

    def test_delete_budget(self):
        variables = {
            "account_name": "KCB test account",
            "account_type": "Savings",
            "account_balance": 20000.00,
            "currency_code": "USD",
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": create_account_mutation,
                       "variables": variables}),
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
            json.dumps({"query": create_budget_mutation,
                       "variables": variables}),
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
            json.dumps({"query": create_account_mutation,
                       "variables": variables}),
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
            json.dumps({"query": create_target_mutation,
                       "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            f"Something went wrong, {explain_status_code(response.status_code)}",
        )

        self.assertEqual(data["data"]["createTarget"]
                         ["target_name"], "Test target")
        self.assertEqual(
            data["data"]["createTarget"]["target_description"],
            "Test target description",
        )
        self.assertEqual(data["data"]["createTarget"]
                         ["target_amount"], 5000.00)
        self.assertEqual(data["data"]["createTarget"]
                         ["target_is_active"], True)
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
            json.dumps({"query": create_account_mutation,
                       "variables": variables}),
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
            json.dumps({"query": create_target_mutation,
                       "variables": variables}),
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

        self.assertEqual(data["data"]["updateTarget"]
                         ["target_name"], "New target")
        self.assertEqual(
            data["data"]["updateTarget"]["target_description"],
            "New target description",
        )
        self.assertEqual(data["data"]["updateTarget"]
                         ["target_amount"], 2500.00)

    def test_delete_target(self):
        variables = {
            "account_name": "KCB test account",
            "account_type": "Savings",
            "account_balance": 20000.00,
            "currency_code": "USD",
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": create_account_mutation,
                       "variables": variables}),
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
            json.dumps({"query": create_target_mutation,
                       "variables": variables}),
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
            json.dumps({"query": create_account_mutation,
                       "variables": variables}),
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
            json.dumps({"query": create_transaction_mutation,
                       "variables": variables}),
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
            json.dumps({"query": create_account_mutation,
                       "variables": variables}),
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
            json.dumps({"query": create_transaction_mutation,
                       "variables": variables}),
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
            json.dumps({"query": create_account_mutation,
                       "variables": variables}),
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
            json.dumps({"query": create_transaction_mutation,
                       "variables": variables}),
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


class TestAppQueries(TestCase):
    def setUp(self) -> None:
        self.client = Client()

        self.package = Package.objects.create(name="Free")

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

    def tearDown(self) -> None:
        self.client.logout()

        self.package.delete()

        self.test_username = None

        self.token = None
