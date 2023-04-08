from django.db.models import Q
from django.conf import settings
from django.core.mail import send_mail
from users.models import Profile, Package
from ariadne_jwt.decorators import login_required
from billing.models import (
    CardPaymentMethod,
    MpesaPaymentMethod,
    CardBilling,
    MpesaBilling,
)


@login_required
def resolve_registerCard(
    _, info, cardholder_name, card_number, expiration_month, expiration_year, cvc
):
    request = info.context["request"]

    card = CardPaymentMethod.objects.create(
        user=request.user,
        cardholder_name=cardholder_name,
        card_number=card_number,
        expiration_month=expiration_month,
        expiration_year=expiration_year,
        cvc=cvc,
    )

    return card


@login_required
def resolve_registerAndBillCard(
    _,
    info,
    cardholder_name,
    card_number,
    expiration_month,
    expiration_year,
    cvc,
    plan,
    amount,
):
    request = info.context["request"]

    card = CardPaymentMethod.objects.create(
        user=request.user,
        cardholder_name=cardholder_name,
        card_number=card_number,
        expiration_month=expiration_month,
        expiration_year=expiration_year,
        cvc=cvc,
    )

    billing = CardBilling.objects.create(
        customer=card, transaction_uid="lksdlfsjdlf", plan=plan, amount=amount
    )

    new_plan = Package.objects.filter(Q(name__exact=plan)).first()

    profile = Profile.objects.get(user__id=request.user.id)

    profile.is_paid_user = True

    profile.payment_method = "Card"

    profile.package = new_plan  # type: ignore

    profile.save()

    subject = f"Billing for {billing.plan} plan."
    body = f"This is your first billing for the {billing.plan} plan.\n You are now subscribed to the {billing.plan} plan.\nAmount paid: {billing.amount}\nTransaction UID: {billing.transaction_uid}\n\n Thank you for your subscription."
    me = settings.DEFAULT_FROM_EMAIL
    recipient = request.user.email

    send_mail(
        subject,
        body,
        me,
        [recipient],
        fail_silently=False,
    )

    return billing


@login_required
def resolve_registerMpesa(_, info, phone_owner, phone_number):
    request = info.context["request"]

    mpesa = MpesaPaymentMethod.objects.create(
        user=request.user, phone_owner=phone_owner, phone_number=phone_number
    )

    return mpesa


@login_required
def resolve_registerAndBillMpesa(_, info, phone_owner, phone_number, plan, amount):
    request = info.context["request"]

    mpesa = MpesaPaymentMethod.objects.create(
        user=request.user, phone_owner=phone_owner, phone_number=phone_number
    )

    billing = MpesaBilling.objects.create(
        customer=mpesa, transaction_uid="lksdlfsjdlf", plan=plan, amount=amount
    )

    new_plan = Package.objects.filter(Q(name__exact=plan)).first()

    profile = Profile.objects.get(user__id=request.user.id)

    profile.is_paid_user = True

    profile.payment_method = "Mpesa"

    profile.package = new_plan  # type: ignore

    profile.save()

    subject = f"Billing for {billing.plan} plan."
    body = f"This is your first billing for the {billing.plan} plan.\n You are now subscribed to the {billing.plan} plan.\nAmount paid: {billing.amount}\nTransaction UID: {billing.transaction_uid}\n\n Thank you for your subscription."
    me = settings.DEFAULT_FROM_EMAIL
    recipient = request.user.email

    send_mail(
        subject,
        body,
        me,
        [recipient],
        fail_silently=False,
    )

    return billing


@login_required
def resolve_requestBilling(_, info, payment_method):
    request = info.context["request"]

    profile = Profile.objects.get(user__id=request.user.id)

    try:
        assert profile.payment_method == payment_method

    except Exception as e:
        raise Exception(str(e))

    if payment_method == "Card":
        card_user = CardPaymentMethod.objects.get(user__id=request.user.id)

        billing = CardBilling.objects.filter(customer=card_user).all()

        html_body = ""

        for bill in billing:
            html_body += f"<tr><td>{bill.transaction_uid}</td><td>{bill.plan}</td><td>{bill.amount}</td><td>{bill.created_at}</td></tr>"

        subject = f"Billing History"
        body = f"This is a summary of your billing history."
        me = settings.DEFAULT_FROM_EMAIL
        recipient = request.user.email
        html_message = f"<html><body><h1>{subject}</h1><br/><table><thead><tr><th>Transaction UID</th><th>Plan</th><th>Amount</th><th>Date</th></tr></thead><tbody>{html_body}</tbody></table></body></html>"

        send_mail(
            subject,
            body,
            me,
            [recipient],
            html_message=html_message,
            fail_silently=False,
        )

    elif payment_method == "Mpesa":
        mpesa_user = MpesaPaymentMethod.objects.get(user__id=request.user.id)

        billing = MpesaBilling.objects.filter(customer=mpesa_user).all()

        html_body = ""

        for bill in billing:
            html_body += f"<tr><td>{bill.transaction_uid}</td><td>{bill.plan}</td><td>{bill.amount}</td><td>{bill.created_at}</td></tr>"

        subject = f"Billing History"
        body = f"This is a summary of your billing history."
        me = settings.DEFAULT_FROM_EMAIL
        recipient = request.user.email
        html_message = f"<html><body><h1>{subject}</h1><br/><table><thead><tr><th>Transaction UID</th><th>Plan</th><th>Amount</th><th>Date</th></tr></thead><tbody>{html_body}</tbody></table></body></html>"

        send_mail(
            subject,
            body,
            me,
            [recipient],
            html_message=html_message,
            fail_silently=False,
        )

    return True


@login_required
def resolve_cancelPlan(_, info, payment_method):
    request = info.context["request"]

    profile = Profile.objects.get(user__id=request.user.id)

    try:
        assert profile.payment_method == payment_method

    except Exception as e:
        raise Exception(str(e))

    if payment_method == "Card":
        card_user = CardPaymentMethod.objects.get(user__id=request.user.id)

        card_user.delete()

        old_plan = Package.objects.filter(Q(name__exact="Free")).first()

        profile.payment_method = "None"

        profile.is_paid_user = False

        profile.package = old_plan  # type: ignore

        profile.save()

    elif payment_method == "Mpesa":
        mpesa_user = MpesaPaymentMethod.objects.get(user__id=request.user.id)

        mpesa_user.delete()

        old_plan = Package.objects.filter(Q(name__exact="Free")).first()

        profile.payment_method = "None"

        profile.is_paid_user = False

        profile.package = old_plan  # type: ignore

        profile.save()

    return True
