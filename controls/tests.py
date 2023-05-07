import json
from uuid import uuid4
from plans.models import Plan
from users.models import User, Profile
from django.test import TestCase, Client
from controls.test_ref import explain_status_code

from controls.mutation_ref import token_auth
from controls.query_ref import (
    test_standard_decorator,
    test_pro_decorator,
    test_if_is_employee,
)


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
            plan=self.standard_plan,
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
            plan=self.pro_plan,
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
                    "query": token_auth,
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
                    "query": token_auth,
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
        variables = {}

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": test_standard_decorator, "variables": variables}),
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
        variables = {}

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": test_pro_decorator, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.test_user_two_token}",
        )

        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            f"Something went wrong, {explain_status_code(response.status_code)}",
        )

        self.assertEqual(data["data"]["testProDecorator"]["name"], "Pro")

    def test_check_if_employee(self):
        variables = {}

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": test_if_is_employee, "variables": variables}),
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
