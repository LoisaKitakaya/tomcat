import json
from uuid import uuid4
from ariadne import gql
from django.test import TestCase, Client
from users.models import User, Profile, Package


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
