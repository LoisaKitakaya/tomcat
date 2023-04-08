from ariadne_jwt.decorators import login_required
from billing.models import (
    CardPaymentMethod,
    MpesaPaymentMethod,
    CardBilling,
    MpesaBilling,
)


@login_required
def resolve_getAllCardUsers(*_):
    card_users = CardPaymentMethod.objects.all()

    return card_users


@login_required
def resolve_getCardUser(_, info):
    request = info.context["request"]

    card_user = CardPaymentMethod.objects.get(user__id=request.user.id)

    return card_user


@login_required
def resolve_getAllMpesaUsers(*_):
    mpesa_users = MpesaPaymentMethod.objects.all()  # type: ignore

    return mpesa_users


@login_required
def resolve_getMpesaUser(_, info):
    request = info.context["request"]

    mpesa_user = MpesaPaymentMethod.objects.get(user__id=request.user.id)

    return mpesa_user


@login_required
def resolve_getAllCardPayments(*_):
    card_payments = CardBilling.objects.all()

    return card_payments


@login_required
def resolve_getUserCardPayments(_, info):
    request = info.context["request"]

    customer = CardPaymentMethod.objects.get(user__id=request.user.id)

    user_payments = CardBilling.objects.filter(customer__id=customer.pk).all()

    return user_payments


@login_required
def resolve_getAllMpesaPayments(*_):
    mpesa_payments = MpesaBilling.objects.all()

    return mpesa_payments


@login_required
def resolve_getUserMpesaPayments(_, info):
    request = info.context["request"]

    customer = MpesaPaymentMethod.objects.get(user__id=request.user.id)

    user_payments = MpesaBilling.objects.filter(customer__id=customer.pk).all()

    return user_payments
