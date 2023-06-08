from users.models import Profile
from ariadne_jwt.decorators import login_required
from invoice.models import PaymentAccount, ClientInformation, Invoice


@login_required
def resolve_getAllPaymentAccounts(_, info):
    request = info.context["request"]

    profile = Profile.objects.get(user__id=request.user.id)

    all_payment_accounts = PaymentAccount.objects.filter(owner__id=profile.pk).all()

    return all_payment_accounts


@login_required
def resolve_getPaymentAccount(*_, id):
    try:
        payment_account = PaymentAccount.objects.get(id=id)

    except Exception as e:
        raise Exception(str(e))

    return payment_account


@login_required
def resolve_getAllClientInformation(_, info):
    request = info.context["request"]

    profile = Profile.objects.get(user__id=request.user.id)

    all_clients = ClientInformation.objects.filter(owner__id=profile.pk).all()

    return all_clients


@login_required
def resolve_getClientInformation(*_, id):
    try:
        client = ClientInformation.objects.get(id=id)

    except Exception as e:
        raise Exception(str(e))

    return client


@login_required
def resolve_getAllInvoices(_, info):
    request = info.context["request"]

    profile = Profile.objects.get(user__id=request.user.id)

    all_invoices = Invoice.objects.filter(owner__id=profile.pk).all()

    return all_invoices


@login_required
def resolve_getInvoice(*_, id):
    try:
        invoice = Invoice.objects.get(id=id)

    except Exception as e:
        raise Exception(str(e))

    return invoice
