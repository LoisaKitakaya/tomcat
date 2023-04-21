import json
from uuid import uuid4
from ariadne import gql
from teams.models import Workspace
from users.models import Package, User
from django.test import TestCase, Client

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

create_team_member_mutation = gql(
    """
    mutation(
        $email: String!
        $first_name: String!
        $last_name: String!
        $password: String!
        ) {
        createTeamMember(
            email: $email
            first_name: $first_name
            last_name: $last_name
            password: $password
        ) {
            id
            first_name
            last_name
            email
            username
            is_staff
            is_active
        }
    }
    """
)


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

    def tearDown(self) -> None:
        self.client.logout()

        self.package.delete()

        self.test_username = None

        self.token = None

    def test_update_workspace(self):
        mutation = gql(
            """
            mutation($name: String!) {
                updateWorkspace(name: $name) {
                    name
                    workspace_uid
                    owner {
                    username
                    }
                }
            }
            """
        )

        variables = {"name": "New Workspace Name"}

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

        self.assertIsNotNone(data["data"]["updateWorkspace"]["workspace_uid"])
        self.assertEqual(data["data"]["updateWorkspace"]["name"], "New Workspace Name")
        self.assertEqual(
            data["data"]["updateWorkspace"]["owner"]["username"], "example@gmail.com"
        )

    def test_create_team_member(self):
        variables = {
            "email": "employee@gmail.com",
            "first_name": "New",
            "last_name": "Employee",
            "password": "#TestUser15",
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": create_team_member_mutation, "variables": variables}),
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
            data["data"]["createTeamMember"]["email"], "employee@gmail.com"
        )
        self.assertEqual(
            data["data"]["createTeamMember"]["username"], "employee@gmail.com"
        )
        self.assertEqual(data["data"]["createTeamMember"]["first_name"], "New")
        self.assertEqual(data["data"]["createTeamMember"]["last_name"], "Employee")
        self.assertEqual(data["data"]["createTeamMember"]["is_staff"], False)
        self.assertEqual(data["data"]["createTeamMember"]["is_active"], True)

    def test_delete_team_member(self):
        variables = {
            "email": "employee@gmail.com",
            "first_name": "New",
            "last_name": "Employee",
            "password": "#TestUser15",
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": create_team_member_mutation, "variables": variables}),
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
            mutation($member_id: ID!) {
                deleteTeamMember(member_id: $member_id)
            }
            """
        )

        variables = {"member_id": str(data["data"]["createTeamMember"]["id"])}

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

        self.assertEqual(data["data"]["deleteTeamMember"], True)


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

        self.test_user = User.objects.create(
            username="test_user", email="test_user@example.com"
        )
        self.test_user.set_password("#testpassword")
        self.test_user.save()

        self.workspace = Workspace.objects.create(
            name="Test Workspace", owner=self.test_user
        )
        self.workspace.workspace_uid = str(uuid4().hex)
        self.workspace.save()

    def tearDown(self) -> None:
        self.client.logout()

        self.package.delete()

        self.test_username = None

        self.token = None

        self.test_user.delete()

        self.workspace.delete()

    def test_get_workspace(self):
        query = gql(
            """
            query {
                getWorkspace {
                    name
                    workspace_uid
                    owner {
                    username
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

        self.assertEqual(data["data"]["getWorkspace"]["name"], "Important Workspace")
        self.assertEqual(
            data["data"]["getWorkspace"]["owner"]["username"], "example@gmail.com"
        )
        self.assertIsNotNone(data["data"]["getWorkspace"]["workspace_uid"])

    def test_get_team_logs(self):
        query = gql(
            """
            query($workspace_id: ID!) {
                getTeamLogs(workspace_id: $workspace_id) {
                    workspace {
                    name
                    }
                    user {
                    username
                    }
                    action
                }
            }
            """
        )

        variables = {"workspace_id": self.workspace.pk}

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

        self.assertListEqual(data["data"]["getTeamLogs"], [])

    def test_get_team_members(self):
        query = gql(
            """
            query {
                getTeamMembers {
                    user {
                    username
                    }
                    package {
                    name
                    }
                    phone_number
                    workspace_uid
                    payment_method
                    is_paid_user
                    is_employee
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

        for member in data["data"]["getTeamMembers"]:
            self.assertEqual(member["user"]["username"], "example@gmail.com")
            self.assertEqual(member["package"]["name"], "Free")
            self.assertIsNotNone(member["workspace_uid"])
