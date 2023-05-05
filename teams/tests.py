import json
from uuid import uuid4
from users.models import User
from plans.models import Plan
from teams.models import Workspace
from django.test import TestCase, Client
from controls.test_ref import explain_status_code

from controls.mutation_ref import (
    token_auth,
    create_user,
    update_workspace,
    create_team_member,
    delete_team_member,
)
from controls.query_ref import get_workspace, get_team_logs, get_team_members


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

    def test_update_workspace(self):
        variables = {"name": "New Workspace Name"}

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": update_workspace, "variables": variables}),
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
            json.dumps({"query": create_team_member, "variables": variables}),
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
            json.dumps({"query": create_team_member, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            f"Something went wrong, {explain_status_code(response.status_code)}",
        )

        variables = {"member_id": str(data["data"]["createTeamMember"]["id"])}

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": delete_team_member, "variables": variables}),
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


class TestQueryMutations(TestCase):
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

        self.plan.delete()

        self.test_username = None

        self.token = None

        self.test_user.delete()

        self.workspace.delete()

    def test_get_workspace(self):
        variables = {}

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": get_workspace, "variables": variables}),
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
        variables = {"workspace_id": self.workspace.pk}

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": get_team_logs, "variables": variables}),
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
        variables = {}

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": get_team_members, "variables": variables}),
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
            self.assertEqual(member["plan"]["name"], "Free")
            self.assertIsNotNone(member["workspace_uid"])
