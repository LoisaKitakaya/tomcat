import json
from users.models import User
from plans.models import Plan
from django.test import TestCase, Client
from controls.test_ref import explain_status_code

from controls.mutation_ref import token_auth, create_user, update_user, verify_otp
from controls.query_ref import get_user, generate_otp, generate_qr_code, get_profile


class Test2FA(TestCase):
    def setUp(self) -> None:
        self.client = Client()

        self.plan = Plan.objects.create(name="Free")

        create_user_variables = {
            "email": "testuser@example.com",
            "first_name": "Test",
            "last_name": "User",
            "workspace_name": "Testing Workspace",
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

    def test_generate_and_verify_OTP(self):
        variables = {"environment": "test"}

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": generate_otp, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            f"Something went wrong, {explain_status_code(response.status_code)}",
        )

        received_otp_code = data["data"]["generateOTP"]["otp_code"]

        self.assertIsNotNone(received_otp_code)

        variables = {"otp": str(received_otp_code)}

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": verify_otp, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            f"Something went wrong, {explain_status_code(response.status_code)}",
        )

        self.assertEqual(data["data"]["verifyOTP"], "Your account has been verified")

    def test_generate_OTP_QRcode(self):
        variables = {}

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": generate_qr_code, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            f"Something went wrong, {explain_status_code(response.status_code)}",
        )

        self.assertIsNotNone(data["data"]["generateQRCode"])
        self.assertEqual(
            type(data["data"]["generateQRCode"]), type("is of type string")
        )


class TestAppMutations(TestCase):
    def setUp(self) -> None:
        self.client = Client()

        self.plan = Plan.objects.create(name="Free")

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
            json.dumps({"query": token_auth, "variables": token_auth_variables}),
            content_type="application/json",
        )

        self.token = get_token.json()["data"]["tokenAuth"]["token"]

    def tearDown(self) -> None:
        self.client.logout()

        self.plan.delete()

        self.test_user.delete()

        self.token = None

    def test_get_token(self):
        variables = {
            "username": self.test_user.username,
            "password": "#testpassword",
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": token_auth, "variables": variables}),
            content_type="application/json",
        )

        token = response.json()["data"]["tokenAuth"]["token"]

        self.assertEqual(
            response.status_code,
            200,
            f"Something went wrong, {explain_status_code(response.status_code)}",
        )

        self.assertIsNotNone(token, "Did not get token")

    def test_create_user(self):
        variables = {
            "email": "testuser@example.com",
            "first_name": "Test",
            "last_name": "User",
            "workspace_name": "Testing Workspace",
            "password": "#TestUser15",
            "password2": "#TestUser15",
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": create_user, "variables": variables}),
            content_type="application/json",
        )

        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            f"Something went wrong, {explain_status_code(response.status_code)}",
        )

        self.assertEqual(data["data"]["createUser"]["email"], "testuser@example.com")
        self.assertEqual(data["data"]["createUser"]["username"], "testuser@example.com")
        self.assertEqual(data["data"]["createUser"]["first_name"], "Test")
        self.assertEqual(data["data"]["createUser"]["last_name"], "User")
        self.assertEqual(data["data"]["createUser"]["is_staff"], False)
        self.assertEqual(data["data"]["createUser"]["is_active"], True)

    def test_update_user(self):
        variables = {
            "email": "user_test@example.com",
            "first_name": "test",
            "last_name": "user",
        }

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": update_user, "variables": variables}),
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

    def test_get_user(self):
        variables = {}

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": get_user, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            f"Something went wrong, {explain_status_code(response.status_code)}",
        )

        self.assertEqual(data["data"]["getUser"]["email"], "example@gmail.com")
        self.assertEqual(data["data"]["getUser"]["username"], "example@gmail.com")
        self.assertEqual(data["data"]["getUser"]["first_name"], "Test")
        self.assertEqual(data["data"]["getUser"]["last_name"], "User")
        self.assertEqual(data["data"]["getUser"]["is_staff"], False)
        self.assertEqual(data["data"]["getUser"]["is_active"], True)

    def test_get_profile(self):
        variables = {}

        response = self.client.post(
            "/graphql/",
            json.dumps({"query": get_profile, "variables": variables}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"JWT {self.token}",
        )

        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            f"Something went wrong, {explain_status_code(response.status_code)}",
        )

        self.assertIsNotNone(data["data"]["getProfile"]["workspace_uid"])
        self.assertEqual(data["data"]["getProfile"]["plan"]["name"], "Free")
        self.assertEqual(data["data"]["getProfile"]["phone_number"], "")
        self.assertEqual(data["data"]["getProfile"]["payment_method"], "None")
        self.assertEqual(data["data"]["getProfile"]["is_paid_user"], False)
        self.assertEqual(data["data"]["getProfile"]["is_employee"], False)
