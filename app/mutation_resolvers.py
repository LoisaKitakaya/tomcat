from datetime import datetime
from django.db.models import Q
from users.models import Profile
from teams.models import Workspace
from ariadne_jwt.decorators import login_required
from app.models import Account, Budget, Transaction, Category, Target


@login_required
def resolve_createAccount(
    _, info, account_name, account_type, account_number, account_balance, currency_code
):

    request = info.context["request"]

    owner = Profile.objects.get(user__id=request.user.id)

    workspace = Workspace.objects.get(owner__id=request.user.id)

    new_account = Account.objects.create(
        account_name=account_name,
        account_type=account_type,
        account_number=account_number,
        account_balance=account_balance,
        currency_code=currency_code,
        owner=owner,
        workspace=workspace,
    )

    return new_account


@login_required
def resolve_updateAccount(
    *_, id, account_name, account_type, account_number, account_balance, currency_code
):

    account = Account.objects.get(id=id)

    account.account_name = account_name
    account.account_type = account_type
    account.account_number = account_number
    account.account_balance = account_balance
    account.currency_code = currency_code

    account.save()

    return account


@login_required
def resolve_deleteAccount(*_, id):

    try:

        Account.objects.get(id=id).delete()

    except Exception as e:

        raise Exception(str(e))

    else:

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

    workspace = Workspace.objects.get(owner__id=request.user.id)

    account = Account.objects.get(id=account_id)

    budget_category = Category.objects.filter(Q(category_name__exact=category)).first()

    new_budget = Budget.objects.create(
        budget_name=budget_name,
        budget_description=budget_description,
        budget_amount=budget_amount,
        category=budget_category,
        owner=profile,
        account=account,
        workspace=workspace,
    )

    return new_budget


@login_required
def resolve_updateBudget(
    *_, id, budget_name, budget_description, budget_amount, category
):

    budget = Budget.objects.get(id=id)

    budget_category = Category.objects.filter(Q(category_name__exact=category)).first()

    budget.budget_name = budget_name
    budget.budget_description = budget_description
    budget.budget_amount = budget_amount
    budget.category = budget_category  # type: ignore

    budget.save()

    return budget


@login_required
def resolve_budgetStatus(*_, id, status):

    budget = Budget.objects.get(id=id)

    budget.budget_is_active = status

    budget.save()

    return True


@login_required
def resolve_deleteBudget(*_, id):

    try:

        Budget.objects.get(id=id).delete()

    except Exception as e:

        raise Exception(str(e))

    else:

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

    workspace = Workspace.objects.get(owner__id=request.user.id)

    account = Account.objects.get(id=account_id)

    target_category = Category.objects.filter(Q(category_name__exact=category)).first()

    new_target = Target.objects.create(
        target_name=target_name,
        target_description=target_description,
        target_amount=target_amount,
        category=target_category,
        owner=profile,
        account=account,
        workspace=workspace,
    )

    return new_target


@login_required
def resolve_updateTarget(
    *_, id, target_name, target_description, target_amount, category
):

    target = Target.objects.get(id=id)

    target_category = Category.objects.filter(Q(category_name__exact=category)).first()

    target.target_name = target_name
    target.target_description = target_description
    target.target_amount = target_amount
    target.category = target_category  # type: ignore

    target.save()

    return target


@login_required
def resolve_targetStatus(*_, id, status):

    target = Target.objects.get(id=id)

    target.target_is_active = status

    target.save()

    return True


@login_required
def resolve_deleteTarget(*_, id):

    try:

        Target.objects.get(id=id).delete()

    except Exception as e:

        raise Exception(str(e))

    else:

        return True


@login_required
def resolve_createTransaction(
    *_,
    account_id,
    transaction_type,
    transaction_amount,
    transaction_date,
    currency_code,
    description,
    category
):

    account = Account.objects.get(id=account_id)

    transaction_category = Category.objects.filter(
        Q(category_name__exact=category)
    ).first()

    date_object = datetime.strptime(transaction_date, "%Y-%m-%d").date()

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

    return new_transaction


@login_required
def resolve_updateTransaction(
    *_,
    id,
    account_id,
    transaction_type,
    transaction_amount,
    transaction_date,
    currency_code,
    description,
    category
):

    account = Account.objects.get(id=account_id)

    transaction = Transaction.objects.get(id=id)

    transaction_category = Category.objects.filter(
        Q(category_name__exact=category)
    ).first()

    date_object = datetime.strptime(transaction_date, "%Y-%m-%d").date()

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
    transaction.category = transaction_category  # type: ignore

    transaction.save()

    return transaction


@login_required
def resolve_deleteTransaction(*_, id, account_id):

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

    return True
