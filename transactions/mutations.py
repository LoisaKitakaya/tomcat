from datetime import datetime
from django.utils import timezone
from accounts.models import Account
from ariadne_jwt.decorators import login_required
from transactions.models import (
    Transaction,
    TransactionType,
    TransactionCategory,
    TransactionSubCategory,
)


@login_required
def resolve_createTransaction(
    *_,
    account_id,
    transaction_type: str,
    transaction_amount: str,
    transaction_date: str,
    description: str,
    category: str,
    sub_category: str,
):
    account = Account.objects.get(id=account_id)

    type = TransactionType.objects.get(type_name=transaction_type)

    transaction_category = TransactionCategory.objects.get(category_name=category)
    transaction_sub_category = TransactionSubCategory.objects.get(
        category_name=sub_category
    )

    date_object = datetime.strptime(transaction_date, "%Y-%m-%dT%H:%M")
    date_object = timezone.make_aware(date_object, timezone.get_default_timezone())

    new_transaction = Transaction.objects.create(
        transaction_type=type,
        transaction_amount=float(transaction_amount),
        transaction_date=date_object,
        currency_code=account.currency_code,
        description=description,
        category=transaction_category,
        sub_category=transaction_sub_category,
        account=account,
    )

    if transaction_type == "payable":
        account.account_balance -= float(transaction_amount)

        account.save()

    elif transaction_type == "receivable":
        account.account_balance += float(transaction_amount)

        account.save()

    return new_transaction


@login_required
def resolve_updateTransaction(
    *_,
    id,
    account_id,
    transaction_type: str,
    transaction_amount: str,
    transaction_date: str,
    description: str,
    category: str,
    sub_category: str,
):
    account = Account.objects.get(id=account_id)

    transaction = Transaction.objects.get(id=id)

    type = (
        TransactionType.objects.get(type_name=transaction_type)
        if transaction_type
        else transaction.transaction_type
    )

    transaction_category = (
        TransactionCategory.objects.get(category_name=category)
        if category
        else transaction.category
    )

    transaction_sub_category = (
        TransactionSubCategory.objects.get(category_name=sub_category)
        if sub_category
        else transaction.sub_category
    )

    if transaction_date:
        date_object = datetime.strptime(transaction_date, "%Y-%m-%dT%H:%M")
        date_object = timezone.make_aware(date_object, timezone.get_default_timezone())

    else:
        date_object = transaction.transaction_date

    if (
        not transaction_type
        and transaction.transaction_type.type_name == "payable"
        or transaction_type == "payable"
        and transaction.transaction_type.type_name == "payable"
    ):
        previous_balance = account.account_balance + transaction.transaction_amount

        account.account_balance = (
            previous_balance - float(transaction_amount)
            if transaction_amount
            else transaction.transaction_amount
        )

        account.save()

    elif (
        not transaction_type
        and transaction.transaction_type.type_name == "receivable"
        or transaction_type == "receivable"
        and transaction.transaction_type.type_name == "receivable"
    ):
        previous_balance = account.account_balance - transaction.transaction_amount

        account.account_balance = (
            previous_balance + float(transaction_amount)
            if transaction_amount
            else transaction.transaction_amount
        )

        account.save()

    elif (
        not transaction_type
        and transaction.transaction_type.type_name == "receivable"
        or transaction_type == "payable"
        and transaction.transaction_type.type_name == "receivable"
    ):
        previous_balance = account.account_balance - transaction.transaction_amount

        account.account_balance = (
            previous_balance - float(transaction_amount)
            if transaction_amount
            else transaction.transaction_amount
        )

        account.save()

    elif (
        not transaction_type
        and transaction.transaction_type.type_name == "payable"
        or transaction_type == "receivable"
        and transaction.transaction_type.type_name == "payable"
    ):
        previous_balance = account.account_balance + transaction.transaction_amount

        account.account_balance = (
            previous_balance + float(transaction_amount)
            if transaction_amount
            else transaction.transaction_amount
        )

        account.save()

    transaction.transaction_type = type
    transaction.transaction_amount = (
        float(transaction_amount)
        if transaction_amount
        else transaction.transaction_amount
    )
    transaction.transaction_date = date_object
    transaction.description = description if description else transaction.description
    transaction.category = transaction_category
    transaction.sub_category = transaction_sub_category

    transaction.save()

    return transaction


@login_required
def resolve_deleteTransaction(*_, id, account_id):
    account = Account.objects.get(id=account_id)

    transaction = Transaction.objects.get(id=id)

    type_payable = TransactionType.objects.get(type_name="payable")
    type_receivable = TransactionType.objects.get(type_name="receivable")

    if transaction.transaction_type == type_payable:
        previous_balance = account.account_balance + transaction.transaction_amount

        account.account_balance = previous_balance

        account.save()

    elif transaction.transaction_type == type_receivable:
        previous_balance = account.account_balance - transaction.transaction_amount

        account.account_balance = previous_balance

        account.save()

    transaction.delete()

    return True
