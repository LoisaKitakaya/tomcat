from django.db.models import Q
from django.conf import settings
from users.models import User, Profile, Package
from ariadne_jwt.decorators import login_required
from billing.models import PlanBilling
from billing.pesapal import PesaPal


@login_required
def resolve_subscribeToPlan(_, info, plan):
    request = info.context["request"]
    amount = 0.00
    currency = "USD"
    description = ""

    if plan == "Standard":
        amount = 10.00
        description = "Subscription payment for Standard plan"

    elif plan == "Pro":
        amount = 15.00
        description = "Subscription payment for Pro plan"

    consumer_key = settings.CONSUMER_KEY
    consumer_secret = settings.CONSUMER_SECRET
    app_url = settings.BACKEND_TRUSTED_URL

    ipn_callback_url = f"{app_url}:8000/billing/pesapal_ipn_callback/"
    notification_callback_url = f"{app_url}:8000/billing/notifications/"

    subscription = PesaPal(
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        notification_url=ipn_callback_url,
        environment="test",
    )

    subscription_payment = subscription.submit_recurring_order_request(
        currency=currency,
        amount=amount,
        description=description,
        callback_url=notification_callback_url,
        email_address=request.user.email,
        first_name=request.user.first_name,
        last_name=request.user.last_name,
    )

    order_tracking_id = subscription_payment["order_tracking_id"]  # type: ignore
    merchant_ref = subscription_payment["merchant_reference"]  # type: ignore
    redirect_url = subscription_payment["redirect_url"]  # type: ignore

    new_billing = PlanBilling.objects.create(
        customer=request.user,
        order_tracking_id=order_tracking_id,
        merchant_ref=merchant_ref,
        redirect_url=redirect_url,
        plan=plan,
        currency=currency,
        amount=amount,
    )

    return new_billing
