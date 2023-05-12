from datetime import datetime
from users.models import Profile
from django.utils import timezone
from accounts.models import Account
from teams.models import Workspace, TeamLogs
from ariadne_jwt.decorators import login_required
from transactions.models import (
    Transaction,
    TransactionType,
    TransactionCategory,
    TransactionSubCategory,
)


@login_required
def resolve_createTransaction(
    _,
    info,
    account_id,
    transaction_type,
    transaction_amount,
    transaction_date,
    description,
    category,
    sub_category,
):
    request = info.context["request"]

    profile = Profile.objects.get(user__id=request.user.id)

    workspace = Workspace.objects.get(workspace_uid=profile.workspace_uid)

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
        transaction_amount=transaction_amount,
        transaction_date=date_object,
        currency_code=account.currency_code,
        description=description,
        category=transaction_category,
        sub_category=transaction_sub_category,
        account=account,
    )

    if transaction_type == "payable":
        account.account_balance -= transaction_amount

        account.save()

    elif transaction_type == "receivable":
        account.account_balance += transaction_amount

        account.save()

    if profile.is_employee:
        TeamLogs.objects.create(
            workspace=workspace,
            user=request.user,
            action=f"Created transaction of ID: {new_transaction.pk}, \
                in account: {account.account_name}",
        )

    return new_transaction


@login_required
def resolve_updateTransaction(
    _,
    info,
    id,
    account_id,
    transaction_type,
    transaction_amount,
    transaction_date,
    description,
    category,
    sub_category,
):
    request = info.context["request"]

    profile = Profile.objects.get(user__id=request.user.id)

    workspace = Workspace.objects.get(workspace_uid=profile.workspace_uid)

    account = Account.objects.get(id=account_id)

    transaction = Transaction.objects.get(id=id)

    type = TransactionType.objects.get(type_name=transaction_type)

    transaction_category = TransactionCategory.objects.get(category_name=category)
    transaction_sub_category = TransactionSubCategory.objects.get(
        category_name=sub_category
    )

    date_object = datetime.strptime(transaction_date, "%Y-%m-%dT%H:%M")
    date_object = timezone.make_aware(date_object, timezone.get_default_timezone())

    if (
        transaction_type == "payable"
        and transaction.transaction_type.type_name == "payable"
    ):
        previous_balance = account.account_balance + transaction.transaction_amount

        account.account_balance = previous_balance - transaction_amount

        account.save()

    elif (
        transaction_type == "receivable"
        and transaction.transaction_type.type_name == "receivable"
    ):
        previous_balance = account.account_balance - transaction.transaction_amount

        account.account_balance = previous_balance + transaction_amount

        account.save()

    elif (
        transaction_type == "payable"
        and transaction.transaction_type.type_name == "receivable"
    ):
        previous_balance = account.account_balance - transaction.transaction_amount

        account.account_balance = previous_balance - transaction_amount

        account.save()

    elif (
        transaction_type == "receivable"
        and transaction.transaction_type.type_name == "payable"
    ):
        previous_balance = account.account_balance + transaction.transaction_amount

        account.account_balance = previous_balance + transaction_amount

        account.save()

    transaction.transaction_type = type
    transaction.transaction_amount = transaction_amount
    transaction.transaction_date = date_object
    transaction.description = description
    transaction.category = transaction_category
    transaction.sub_category = transaction_sub_category

    transaction.save()

    if profile.is_employee:
        TeamLogs.objects.create(
            workspace=workspace,
            user=request.user,
            action=f"Created transaction of ID: {transaction.pk}, \
                in account: {account.account_name}",
        )

    return transaction


@login_required
def resolve_deleteTransaction(_, info, id, account_id):
    request = info.context["request"]

    profile = Profile.objects.get(user__id=request.user.id)

    workspace = Workspace.objects.get(workspace_uid=profile.workspace_uid)

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

    if profile.is_employee:
        TeamLogs.objects.create(
            workspace=workspace,
            user=request.user,
            action=f"Deleted transaction of ID: {transaction.pk}, \
                in account: {account.account_name}",
        )

    return True
