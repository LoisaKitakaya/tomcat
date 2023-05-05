import json
import string
import random
import requests
from uuid import uuid4

sandbox_url = "https://cybqa.pesapal.com/pesapalv3"
live_url = "https://pay.pesapal.com/v3"

sandbox_authentication_url = f"{sandbox_url}/api/Auth/RequestToken"
live_authentication_url = f"{live_url}/api/Auth/RequestToken"

sandbox_ipn_registration_url = f"{sandbox_url}/api/URLSetup/RegisterIPN"
live_ipn_registration_url = f"{live_url}/api/URLSetup/RegisterIPN"


def generate_account_number():
    letters_and_digits = string.ascii_uppercase + string.digits
    group_size = 3
    group_count = 3
    groups = [
        "".join(random.choices(letters_and_digits, k=group_size))
        for _ in range(group_count)
    ]
    return "-".join(groups)


def authenticate(consumer_key, consumer_secret, url):
    payload = json.dumps(
        {
            "consumer_key": consumer_key,
            "consumer_secret": consumer_secret,
        }
    )
    headers = {"Content-Type": "application/json", "Accept": "application/json"}

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.json()


def register_ipn_url(notification_url, registration_url, token):
    payload = json.dumps({"url": notification_url, "ipn_notification_type": "POST"})

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }

    response = requests.request("POST", registration_url, headers=headers, data=payload)

    return response.json()


class PesaPal:
    def __init__(
        self,
        consumer_key="",
        consumer_secret="",
        notification_url="",
        environment="",
    ) -> None:
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.notification_url = notification_url
        self.environment = environment

        if self.environment == "test":
            auth_response = authenticate(
                consumer_key=self.consumer_key,
                consumer_secret=self.consumer_secret,
                url=sandbox_authentication_url,
            )

            self.token = auth_response["token"]

            ipn_registration_response = register_ipn_url(
                notification_url=self.notification_url,
                registration_url=sandbox_ipn_registration_url,
                token=self.token,
            )

            self.ipn_id = ipn_registration_response["ipn_id"]

        elif self.environment == "live":
            auth_response = authenticate(
                consumer_key=self.consumer_key,
                consumer_secret=self.consumer_secret,
                url=live_authentication_url,
            )

            self.token = auth_response["token"]

            ipn_registration_response = register_ipn_url(
                notification_url=self.notification_url,
                registration_url=live_ipn_registration_url,
                token=self.token,
            )

            self.ipn_id = ipn_registration_response["ipn_id"]

    def __repr__(self) -> str:  # type: ignore
        return f"Pesapal object \
            <Consumer key: {self.consumer_key}> \
            <Consumer secret: {self.consumer_secret}> \
                <Notification URL: {self.notification_url}> \
                    <IPN ID: {self.ipn_id}> <Environment: {self.environment}>"

    def __str__(self) -> str:  # type: ignore
        return f"Pesapal object \
            <Consumer key: {self.consumer_key}> \
            <Consumer secret: {self.consumer_secret}> \
                <Notification URL: {self.notification_url}> \
                    <IPN ID: {self.ipn_id}> <Environment: {self.environment}>"

    def get_ipn_registered_endpoints(self):
        # get IPN registered endpoints

        sandbox_get_ipn_registered_endpoints = f"{sandbox_url}/api/URLSetup/GetIpnList"
        live_get_ipn_registered_endpoints = f"{live_url}/api/URLSetup/GetIpnList"

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}",
        }

        if self.environment == "test":
            response = requests.request(
                "GET", sandbox_get_ipn_registered_endpoints, headers=headers
            )

            return response.json()

        elif self.environment == "live":
            response = requests.request(
                "GET", live_get_ipn_registered_endpoints, headers=headers
            )

            return response.json()

    def submit_order_request(
        self,
        currency,
        amount,
        description,
        callback_url,
        email_address,
        first_name,
        last_name,
        phone_number=None,
        country_code=None,
        middle_name=None,
        line_1=None,
        line_2=None,
        city=None,
        state=None,
        postal_code=None,
        zip_code=None,
    ):
        # submit order request

        sandbox_submit_order_request = (
            f"{sandbox_url}/api/Transactions/SubmitOrderRequest"
        )
        live_submit_order_request = f"{live_url}/api/Transactions/SubmitOrderRequest"

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}",
        }

        payload = json.dumps(
            {
                "id": str(uuid4().hex),
                "currency": currency,
                "amount": amount,
                "description": description,
                "callback_url": callback_url,
                "notification_id": self.ipn_id,
                "billing_address": {
                    "email_address": email_address,
                    "phone_number": phone_number or "",
                    "country_code": country_code or "",
                    "first_name": first_name,
                    "middle_name": middle_name or "",
                    "last_name": last_name,
                    "line_1": line_1 or "",
                    "line_2": line_2 or "",
                    "city": city or "",
                    "state": state or "",
                    "postal_code": postal_code or "",
                    "zip_code": zip_code or "",
                },
            }
        )

        if self.environment == "test":
            response = requests.request(
                "POST", sandbox_submit_order_request, headers=headers, data=payload
            )

            return response.json()

        elif self.environment == "live":
            response = requests.request(
                "POST", live_submit_order_request, headers=headers, data=payload
            )

            return response.json()

    def submit_recurring_order_request(
        self,
        currency,
        amount,
        description,
        callback_url,
        email_address,
        first_name,
        last_name,
        phone_number=None,
        country_code=None,
        middle_name=None,
        line_1=None,
        line_2=None,
        city=None,
        state=None,
        postal_code=None,
        zip_code=None,
    ):
        # submit order request

        sandbox_submit_order_request = (
            f"{sandbox_url}/api/Transactions/SubmitOrderRequest"
        )
        live_submit_order_request = f"{live_url}/api/Transactions/SubmitOrderRequest"

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}",
        }

        payload = json.dumps(
            {
                "id": str(uuid4().hex),
                "account_number": str(generate_account_number()),
                "currency": currency,
                "amount": amount,
                "description": description,
                "callback_url": callback_url,
                "notification_id": self.ipn_id,
                "billing_address": {
                    "email_address": email_address,
                    "phone_number": phone_number or "",
                    "country_code": country_code or "",
                    "first_name": first_name,
                    "middle_name": middle_name or "",
                    "last_name": last_name,
                    "line_1": line_1 or "",
                    "line_2": line_2 or "",
                    "city": city or "",
                    "state": state or "",
                    "postal_code": postal_code or "",
                    "zip_code": zip_code or "",
                },
            }
        )

        if self.environment == "test":
            response = requests.request(
                "POST", sandbox_submit_order_request, headers=headers, data=payload
            )

            return response.json()

        elif self.environment == "live":
            response = requests.request(
                "POST", live_submit_order_request, headers=headers, data=payload
            )

            return response.json()

    def get_transaction_status(self, order_tracking_id):
        sandbox_get_transaction_status = f"{sandbox_url}/api/Transactions/GetOrderByTrackingId\
            ?orderTrackingId={order_tracking_id}"
        live_get_transaction_status = f"{live_url}/api/Transactions/GetOrderByTrackingId\
            ?orderTrackingId={order_tracking_id}"

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}",
        }

        if self.environment == "test":
            response = requests.request(
                "GET", sandbox_get_transaction_status, headers=headers
            )

            return response.json()

        elif self.environment == "live":
            response = requests.request(
                "GET", live_get_transaction_status, headers=headers
            )

            return response.json()
