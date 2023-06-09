import json
from plans.models import Plan
from users.models import User, Profile
from django.test import TestCase, Client
from controls.test_ref import explain_status_code

from controls.mutation_ref import token_auth
from controls.query_ref import (
    test_pro_decorator,
    test_standard_decorator,
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

        self.test_user_one_profile = Profile.objects.create(
            user=self.test_user_one,
            plan=self.standard_plan,
        )

        self.test_user_two = User.objects.create(
            username="testusertwo", email="testusertwo@example.com"
        )
        self.test_user_two.set_password("#testpassword")
        self.test_user_two.save()

        self.test_user_two_profile = Profile.objects.create(
            user=self.test_user_two,
            plan=self.pro_plan,
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
