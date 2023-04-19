from datetime import datetime
from django.db.models import Q
from users.models import Profile
from teams.models import Workspace, TeamLogs
from ariadne_jwt.decorators import login_required
from app.models import Account, Budget, Transaction, Category, Target


@login_required
def resolve_createAccount(
    _,
    info,
    account_name,
    account_type,
    account_number,
    account_balance,
    currency_code,
):
    request = info.context["request"]

    profile = Profile.objects.get(user__id=request.user.id)

    workspace = Workspace.objects.get(workspace_uid=profile.workspace_uid)

    new_account = Account.objects.create(
        account_name=account_name,
        account_type=account_type,
        account_number=account_number,
        account_balance=account_balance,
        currency_code=currency_code,
        owner=profile,
        workspace=workspace,
    )

    if profile.is_employee:
        TeamLogs.objects.create(
            workspace=workspace,
            user=request.user,
            action=f"Created account: {new_account.account_name}",
        )

    return new_account


@login_required
def resolve_updateAccount(
    _,
    info,
    id,
    account_name,
    account_type,
    account_number,
    account_balance,
    currency_code,
):
    request = info.context["request"]

    profile = Profile.objects.get(user=request.user)

    workspace = Workspace.objects.get(workspace_uid=profile.workspace_uid)

    account = Account.objects.get(id=id)

    account.account_name = account_name
    account.account_type = account_type
    account.account_number = account_number
    account.account_balance = account_balance
    account.currency_code = currency_code

    account.save()

    if profile.is_employee:
        TeamLogs.objects.create(
            workspace=workspace,
            user=request.user,
            action=f"Updated account: {account.account_name}",
        )

    return account


@login_required
def resolve_deleteAccount(_, info, id):
    request = info.context["request"]

    profile = Profile.objects.get(user=request.user)

    workspace = Workspace.objects.get(workspace_uid=profile.workspace_uid)

    try:
        account = Account.objects.get(id=id)

        account_name = account.account_name

        account.delete()

    except Exception as e:
        raise Exception(str(e))

    if profile.is_employee:
        TeamLogs.objects.create(
            workspace=workspace,
            user=request.user,
            action=f"Deleted account: {account_name}",
        )

    return True


@login_required
def resolve_createBudget(
    _,
    info,
    account_id,
    budget_name,
    budget_description,
    budget_amount,
    category,
):
    request = info.context["request"]

    profile = Profile.objects.get(user__id=request.user.id)

    workspace = Workspace.objects.get(workspace_uid=profile.workspace_uid)

    account = Account.objects.get(id=account_id)

    budget_category = Category.objects.get(category_name=category)

    new_budget = Budget.objects.create(
        budget_name=budget_name,
        budget_description=budget_description,
        budget_amount=budget_amount,
        category=budget_category,
        owner=profile,
        account=account,
        workspace=workspace,
    )

    if profile.is_employee:
        TeamLogs.objects.create(
            workspace=workspace,
            user=request.user,
            action=f"Created budget: {new_budget.budget_name}",
        )

    return new_budget


@login_required
def resolve_updateBudget(
    _,
    info,
    id,
    budget_name,
    budget_description,
    budget_amount,
    category,
):
    request = info.context["request"]

    profile = Profile.objects.get(user__id=request.user.id)

    workspace = Workspace.objects.get(workspace_uid=profile.workspace_uid)

    budget = Budget.objects.get(id=id)

    budget_category = Category.objects.get(category_name=category)

    budget.budget_name = budget_name
    budget.budget_description = budget_description
    budget.budget_amount = budget_amount
    budget.category = budget_category

    budget.save()

    if profile.is_employee:
        TeamLogs.objects.create(
            workspace=workspace,
            user=request.user,
            action=f"Updated budget: {budget.budget_name}",
        )

    return budget


@login_required
def resolve_budgetStatus(_, info, id, status):
    request = info.context["request"]

    profile = Profile.objects.get(user__id=request.user.id)

    workspace = Workspace.objects.get(workspace_uid=profile.workspace_uid)

    budget = Budget.objects.get(id=id)

    budget.budget_is_active = status

    budget.save()

    if profile.is_employee:
        TeamLogs.objects.create(
            workspace=workspace,
            user=request.user,
            action=f"Updated budget status to: {status}",
        )

    return True


@login_required
def resolve_deleteBudget(_, info, id):
    request = info.context["request"]

    profile = Profile.objects.get(user__id=request.user.id)

    workspace = Workspace.objects.get(workspace_uid=profile.workspace_uid)

    try:
        budget = Budget.objects.get(id=id)

        budget_name = budget.budget_name

        budget.delete()

    except Exception as e:
        raise Exception(str(e))

    if profile.is_employee:
        TeamLogs.objects.create(
            workspace=workspace,
            user=request.user,
            action=f"Deleted budget: {budget_name}",
        )

    return True


@login_required
def resolve_createTarget(
    _,
    info,
    account_id,
    target_name,
    target_description,
    target_amount,
    category,
):
    request = info.context["request"]

    profile = Profile.objects.get(user__id=request.user.id)

    workspace = Workspace.objects.get(workspace_uid=profile.workspace_uid)

    account = Account.objects.get(id=account_id)

    target_category = Category.objects.get(category_name=category)

    new_target = Target.objects.create(
        target_name=target_name,
        target_description=target_description,
        target_amount=target_amount,
        category=target_category,
        owner=profile,
        account=account,
        workspace=workspace,
    )

    if profile.is_employee:
        TeamLogs.objects.create(
            workspace=workspace,
            user=request.user,
            action=f"Created target: {new_target.target_name}",
        )

    return new_target


@login_required
def resolve_updateTarget(
    _,
    info,
    id,
    target_name,
    target_description,
    target_amount,
    category,
):
    request = info.context["request"]

    profile = Profile.objects.get(user__id=request.user.id)

    workspace = Workspace.objects.get(workspace_uid=profile.workspace_uid)

    target = Target.objects.get(id=id)

    target_category = Category.objects.get(category_name=category)

    target.target_name = target_name
    target.target_description = target_description
    target.target_amount = target_amount
    target.category = target_category

    target.save()

    if profile.is_employee:
        TeamLogs.objects.create(
            workspace=workspace,
            user=request.user,
            action=f"Updated target: {target.target_name}",
        )

    return target


@login_required
def resolve_targetStatus(_, info, id, status):
    request = info.context["request"]

    profile = Profile.objects.get(user__id=request.user.id)

    workspace = Workspace.objects.get(workspace_uid=profile.workspace_uid)

    target = Target.objects.get(id=id)

    target.target_is_active = status

    target.save()

    if profile.is_employee:
        TeamLogs.objects.create(
            workspace=workspace,
            user=request.user,
            action=f"Updated target status to: {status}",
        )

    return True


@login_required
def resolve_deleteTarget(_, info, id):
    request = info.context["request"]

    profile = Profile.objects.get(user__id=request.user.id)

    workspace = Workspace.objects.get(workspace_uid=profile.workspace_uid)

    try:
        target = Target.objects.get(id=id)

        target_name = target.target_name

        target.delete()

    except Exception as e:
        raise Exception(str(e))

    if profile.is_employee:
        TeamLogs.objects.create(
            workspace=workspace,
            user=request.user,
            action=f"Deleted target: {target_name}",
        )

    return True


@login_required
def resolve_createTransaction(
    _,
    info,
    account_id,
    transaction_type,
    transaction_amount,
    transaction_date,
    currency_code,
    description,
    category,
):
    request = info.context["request"]

    profile = Profile.objects.get(user__id=request.user.id)

    workspace = Workspace.objects.get(workspace_uid=profile.workspace_uid)

    account = Account.objects.get(id=account_id)

    transaction_category = Category.objects.get(category_name=category)

    date_object = datetime.strptime(transaction_date, "%Y-%m-%dT%H:%M")

    new_transaction = Transaction.objects.create(
        transaction_type=transaction_type,
        transaction_amount=transaction_amount,
        transaction_date=date_object,
        currency_code=currency_code,
        description=description,
        category=transaction_category,
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
    currency_code,
    description,
    category,
):
    request = info.context["request"]

    profile = Profile.objects.get(user__id=request.user.id)

    workspace = Workspace.objects.get(workspace_uid=profile.workspace_uid)

    account = Account.objects.get(id=account_id)

    transaction = Transaction.objects.get(id=id)

    transaction_category = Category.objects.get(category_name=category)

    date_object = datetime.strptime(transaction_date, "%Y-%m-%dT%H:%M")

    if transaction.transaction_type == "payable" and transaction_type == "payable":
        previous_balance = account.account_balance + transaction.transaction_amount

        account.account_balance = previous_balance - transaction_amount

        account.save()

    elif (
        transaction.transaction_type == "receivable"
        and transaction_type == "receivable"
    ):
        previous_balance = account.account_balance - transaction.transaction_amount

        account.account_balance = previous_balance + transaction_amount

        account.save()

    elif transaction.transaction_type == "receivable" and transaction_type == "payable":
        previous_balance = account.account_balance - transaction.transaction_amount

        account.account_balance = previous_balance - transaction_amount

        account.save()

    elif transaction.transaction_type == "payable" and transaction_type == "receivable":
        previous_balance = account.account_balance + transaction.transaction_amount

        account.account_balance = previous_balance + transaction_amount

        account.save()

    transaction.transaction_type = transaction_type
    transaction.transaction_amount = transaction_amount
    transaction.transaction_date = date_object
    transaction.currency_code = currency_code
    transaction.description = description
    transaction.category = transaction_category

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

    if transaction.transaction_type == "payable":
        previous_balance = account.account_balance + transaction.transaction_amount

        account.account_balance = previous_balance

        account.save()

    elif transaction.transaction_type == "receivable":
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
