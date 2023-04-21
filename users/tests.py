import json
from ariadne import gql
from django.test import TestCase, Client
from users.models import User, Package, Profile, OTPDevice

# Create your tests here.


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


class TestAppFunctions(TestCase):
    pass


class TestAppMutations(TestCase):
    def setUp(self) -> None:
        self.client = Client()

        self.free_package = Package.objects.create(name="Free")

        self.test_user = User.objects.create(
            username="test_user", email="test_user@example.com"
        )
        self.test_user.set_password("#testpassword")
        self.test_user.save()

        token_auth_variables = {
            "username": self.test_user.username,
            "password": "#testpassword",
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

        self.free_package.delete()

        self.test_user.delete()

        self.token = None

    def test_get_token(self):
        variables = {
            "username": self.test_user.username,
            "password": "#testpassword",
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": token_auth_mutation, "variables": variables}),
            content_type="application/json",
        )

        token = response.json()["data"]["tokenAuth"]["token"]

        self.assertEqual(
            response.status_code,
            200,
            f"Something went wrong, {explain_status_code(response.status_code)}",
        )

        self.assertIsNotNone(token, "Did not get token")

    def test_create_user_mutation(self):
        mutation = gql(
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

        variables = {
            "email": "example@gmail.com",
            "first_name": "Test",
            "last_name": "User",
            "workspace_name": "Important Workspace",
            "password": "#TestUser15",
            "password2": "#TestUser15",
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": mutation, "variables": variables}),
            content_type="application/json",
        )

        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            f"Something went wrong, {explain_status_code(response.status_code)}",
        )

        self.assertEqual(data["data"]["createUser"]["email"], "example@gmail.com")
        self.assertEqual(data["data"]["createUser"]["username"], "example@gmail.com")
        self.assertEqual(data["data"]["createUser"]["first_name"], "Test")
        self.assertEqual(data["data"]["createUser"]["last_name"], "User")
        self.assertEqual(data["data"]["createUser"]["is_staff"], False)
        self.assertEqual(data["data"]["createUser"]["is_active"], True)

    def test_update_user_mutation(self):
        mutation = gql(
            """
            mutation($email: String!, $first_name: String!, $last_name: String) {
            updateUser(email: $email, first_name: $first_name, last_name: $last_name) {
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

        variables = {
            "email": "user_test@example.com",
            "first_name": "test",
            "last_name": "user",
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

        self.assertEqual(data["data"]["updateUser"]["email"], "user_test@example.com")
        self.assertEqual(
            data["data"]["updateUser"]["username"], "user_test@example.com"
        )
        self.assertEqual(data["data"]["updateUser"]["first_name"], "test")
        self.assertEqual(data["data"]["updateUser"]["last_name"], "user")
        self.assertEqual(data["data"]["updateUser"]["is_staff"], False)
        self.assertEqual(data["data"]["updateUser"]["is_active"], True)


class TestAppQueries(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def tearDown(self) -> None:
        self.client.logout()
