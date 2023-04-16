from django.db.models import Q
from billing.pesapal import PesaPal
from django.shortcuts import render
from billing.models import PlanBilling
from users.models import User, Profile, Package


def notifications(request):
    if request.method == "POST":
        order_tracking_id = request.GET.get("OrderTrackingId")
        order_merchant_reference = request.GET.get("OrderMerchantReference")
        order_notification_type = request.GET.get("OrderNotificationType")

        print(f"{order_tracking_id}\n")
        print(f"{order_merchant_reference}\n")
        print(f"{order_notification_type}\n")

        context = {
            "order_tracking_id": order_tracking_id,
            "order_merchant_reference": order_merchant_reference,
            order_notification_type: order_notification_type,
        }

        return render(request, "billing/index.html", context=context)


def pesapal_ipn_callback(request):
    if request.method == "POST":
        order_tracking_id = request.GET.get("OrderTrackingId")
        order_merchant_reference = request.GET.get("OrderMerchantReference")
        order_notification_type = request.GET.get("OrderNotificationType")

        print(f"{order_tracking_id}\n")
        print(f"{order_merchant_reference}\n")
        print(f"{order_notification_type}\n")

        return
