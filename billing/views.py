from plans.models import Plan
from django.conf import settings
from users.models import Profile
from django.shortcuts import render
from controls.pesapal import PesaPal
from billing.models import PlanBilling
from django.core.mail import send_mail


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
        order_tracking_id = request.POST.get("OrderTrackingId")
        order_merchant_reference = request.POST.get("OrderMerchantReference")
        order_notification_type = request.POST.get("OrderNotificationType")

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

        print(transaction_status)

        account_ref = transaction_status["subscription_transaction_info"][  # type: ignore
            "account_reference"
        ]

        if (
            transaction_status["status_code"] == 1  # type: ignore
            and transaction_status["status"] == "200"  # type: ignore
        ):
            user_billing = PlanBilling.objects.get(order_tracking_id=order_tracking_id)

            user_billing.account_ref = account_ref if account_ref else "NOT RECURRING"
            user_billing.payment_confirmed = True

            user_billing.save()

            plan = Plan.objects.get(name=user_billing.plan)

            user_profile = Profile.objects.get(user__id=user_billing.customer.pk)

            user_profile.plan = plan
            user_profile.is_paid_user = True
            user_profile.payment_method = transaction_status["payment_method"]  # type: ignore

            user_profile.save()

            payment_status = transaction_status["payment_status"]  # type: ignore
            amount = transaction_status["amount"]  # type: ignore
            currency = transaction_status["currency"]  # type: ignore
            created_date = transaction_status["created_date"]  # type: ignore

            subject = f"Transaction Status"
            body = f"Order tracking ID: {order_tracking_id}\n\
                Payment status: {payment_status}\n\
                    Amount: {amount}\n\
                        Currency: {currency}\n\
                            Account: {user_billing.account_ref}\n\
                                \nCreated date: {created_date}"
            me = settings.DEFAULT_FROM_EMAIL
            recipient = settings.DEFAULT_FROM_EMAIL

            send_mail(
                subject,
                body,
                me,
                [recipient],
                fail_silently=False,
            )

        return
