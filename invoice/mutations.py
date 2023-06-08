from datetime import datetime
from users.models import Profile
from django.utils import timezone
from ariadne_jwt.decorators import login_required
from invoice.models import PaymentAccount, ClientInformation, Invoice
from transactions.models import TransactionCategory, TransactionSubCategory


@login_required
def resolve_createPaymentAccount(
    _,
    info,
    business_name: str,
    business_email: str,
    business_phone_number: str,
    bank_name: str,
    bank_account: str,
    mobile_payment_name: str,
    mobile_account: str,
):
    request = info.context["request"]

    profile = Profile.objects.get(user__id=request.user.id)

    payment_account = PaymentAccount.objects.create(
        owner=profile,
        business_name=business_name,
        business_email=business_email,
        business_phone_number=business_phone_number,
        bank_name=bank_name,
        bank_account=bank_account,
        mobile_payment_name=mobile_payment_name,
        mobile_account=mobile_account,
    )

    return payment_account


@login_required
def resolve_updatePaymentAccount(
    *_,
    id,
    business_name: str,
    business_email: str,
    business_phone_number: str,
    bank_name: str,
    bank_account: str,
    mobile_payment_name: str,
    mobile_account: str,
):
    payment_account = PaymentAccount.objects.get(id=id)

    payment_account.business_name = (
        business_name if business_name else payment_account.business_name
    )
    payment_account.business_email = (
        business_email if business_email else payment_account.business_email
    )
    payment_account.business_phone_number = (
        business_phone_number
        if business_phone_number
        else payment_account.business_phone_number
    )
    payment_account.bank_name = bank_name if bank_name else payment_account.bank_name
    payment_account.bank_account = (
        bank_account if bank_account else payment_account.bank_account
    )
    payment_account.mobile_payment_name = (
        mobile_payment_name
        if mobile_payment_name
        else payment_account.mobile_payment_name
    )
    payment_account.mobile_account = (
        mobile_account if mobile_account else payment_account.mobile_account
    )

    payment_account.save()

    return payment_account


@login_required
def resolve_deletePaymentAccount(*_, id):
    try:
        payment_account = PaymentAccount.objects.get(id=id)

        payment_account.delete()

    except Exception as e:
        raise Exception(str(e))

    return True


@login_required
def resolve_createClientInformation(
    _,
    info,
    client_name: str,
    client_email: str,
    client_phone_number: str,
    client_address: str,
):
    request = info.context["request"]

    profile = Profile.objects.get(user__id=request.user.id)

    client_info = ClientInformation.objects.create(
        owner=profile,
        client_name=client_name,
        client_email=client_email,
        client_phone_number=client_phone_number,
        client_address=client_address,
    )

    return client_info


@login_required
def resolve_updateClientInformation(
    *_,
    id,
    client_name: str,
    client_email: str,
    client_phone_number: str,
    client_address: str,
):
    client = ClientInformation.objects.get(id=id)

    client.client_name = client_name if client_name else client.client_name
    client.client_email = client_email if client_email else client.client_email
    client.client_phone_number = (
        client_phone_number if client_phone_number else client.client_phone_number
    )
    client.client_address = client_address if client_address else client.client_address

    client.save()

    return client


@login_required
def resolve_deleteClientInformation(*_, id):
    try:
        client = ClientInformation.objects.get(id=id)

        client.delete()

    except Exception as e:
        raise Exception(str(e))

    return True


@login_required
def resolve_createInvoice(
    _,
    info,
    business: str,
    client: str,
    category: str,
    sub_category: str,
    item: str,
    quantity: str,
    amount: str,
    additional_notes: str,
    due_date: str,
):
    request = info.context["request"]

    profile = Profile.objects.get(user__id=request.user.id)

    invoice_business = PaymentAccount.objects.get(business_name=business)

    invoice_client = ClientInformation.objects.get(client_name=client)

    transaction_category = TransactionCategory.objects.get(category_name=category)
    transaction_sub_category = TransactionSubCategory.objects.get(
        category_name=sub_category
    )

    date_object = datetime.strptime(due_date, "%Y-%m-%dT%H:%M")
    date_object = timezone.make_aware(date_object, timezone.get_default_timezone())

    invoice_total = int(quantity) * float(amount)

    invoice = Invoice.objects.create(
        owner=profile,
        business=invoice_business,
        client=invoice_client,
        category=transaction_category,
        sub_category=transaction_sub_category,
        item=item,
        quantity=int(quantity),
        amount=float(amount),
        total=invoice_total,
        additional_notes=additional_notes,
        due_date=date_object,
    )

    return invoice


@login_required
def resolve_updateInvoice(
    *_,
    id,
    business: str,
    client: str,
    category: str,
    sub_category: str,
    item: str,
    quantity: str,
    amount: str,
    additional_notes: str,
    due_date: str,
):
    invoice = Invoice.objects.get(id=id)

    invoice_business = (
        PaymentAccount.objects.get(business_name=business)
        if business
        else invoice.business
    )

    invoice_client = (
        ClientInformation.objects.get(client_name=client) if client else invoice.client
    )

    transaction_category = (
        TransactionCategory.objects.get(category_name=category)
        if category
        else invoice.category
    )

    transaction_sub_category = (
        TransactionSubCategory.objects.get(category_name=sub_category)
        if sub_category
        else invoice.sub_category
    )

    if due_date:
        date_object = datetime.strptime(due_date, "%Y-%m-%dT%H:%M")
        date_object = timezone.make_aware(date_object, timezone.get_default_timezone())

    else:
        date_object = invoice.due_date

    if quantity or amount:
        invoice_total = (int(quantity) if quantity else invoice.quantity) * (
            float(amount) if amount else invoice.amount
        )

    else:
        invoice_total = invoice.total

    invoice.business = invoice_business
    invoice.client = invoice_client
    invoice.category = transaction_category
    invoice.sub_category = transaction_sub_category
    invoice.item = item if item else invoice.item
    invoice.quantity = int(quantity) if quantity else invoice.quantity
    invoice.amount = float(amount) if amount else invoice.amount
    invoice.total = invoice_total
    invoice.additional_notes = (
        additional_notes if additional_notes else invoice.additional_notes
    )
    invoice.due_date = date_object

    invoice.save()

    return invoice


@login_required
def resolve_deleteInvoice(*_, id):
    try:
        invoice = Invoice.objects.get(id=id)

        invoice.delete()

    except Exception as e:
        raise Exception(str(e))

    return True
