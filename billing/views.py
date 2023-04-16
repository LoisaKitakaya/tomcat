from django.db.models import Q
from billing.pesapal import PesaPal
from django.shortcuts import render
from billing.models import PlanBilling
from users.models import User, Profile, Package
from django.conf import settings


def notifications(request):
    order_tracking_id = request.GET.get("OrderTrackingId")
    order_merchant_reference = request.GET.get("OrderMerchantReference")
    order_notification_type = request.GET.get("OrderNotificationType")

    print(f"{order_tracking_id}\n")
    print(f"{order_merchant_reference}\n")
    print(f"{order_notification_type}\n")

    context = {
        "order_tracking_id": order_tracking_id,
        "order_merchant_reference": order_merchant_reference,
        "order_notification_type": order_notification_type,
    }

    return render(request, "billing/notifications.html", context=context)


def pesapal_ipn_callback(request):
    if request.method == "POST":
        order_tracking_id = request.GET.get("OrderTrackingId")
        order_merchant_reference = request.GET.get("OrderMerchantReference")
        order_notification_type = request.GET.get("OrderNotificationType")

        print(f"{order_tracking_id}\n")
        print(f"{order_merchant_reference}\n")
        print(f"{order_notification_type}\n")

        consumer_key = settings.CONSUMER_KEY
        consumer_secret = settings.CONSUMER_SECRET
        environment = settings.ENVIRONMENT
        app_url = settings.BACKEND_TRUSTED_URL

        test_ipn_callback_url = f"{app_url}:8000/billing/pesapal_ipn_callback/"

        live_ipn_callback_url = f"{app_url}/billing/pesapal_ipn_callback/"

        transaction = PesaPal(
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            notification_url=live_ipn_callback_url
            if environment == "live"
            else test_ipn_callback_url,
            environment=environment,
        )

        transaction_status = transaction.get_transaction_status(
            order_tracking_id=order_tracking_id
        )

        # transaction status codes

        INVALID = 0
        COMPLETED = 1
        FAILED = 2
        REVERSED = 3

        print(transaction_status)

        return
