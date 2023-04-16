from users.models import Profile
from billing.models import PlanBilling
from billing.pesapal import PesaPal


def notifications(request):
    if request.method == "POST":
        order_tracking_id = request.GET.get("OrderTrackingId")
        order_merchant_reference = request.GET.get("OrderMerchantReference")
        order_notification_type = request.GET.get("OrderNotificationType")

        print(f"{order_tracking_id}\n")
        print(f"{order_merchant_reference}\n")
        print(f"{order_notification_type}\n")

        return


def pesapal_ipn_callback(request):
    if request.method == "POST":
        order_tracking_id = request.GET.get("OrderTrackingId")
        order_merchant_reference = request.GET.get("OrderMerchantReference")
        order_notification_type = request.GET.get("OrderNotificationType")

        print(f"{order_tracking_id}\n")
        print(f"{order_merchant_reference}\n")
        print(f"{order_notification_type}\n")

        return
