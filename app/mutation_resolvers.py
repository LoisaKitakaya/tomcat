import datetime as set_date
from datetime import datetime
from django.db.models import Q
from users.models import Profile
from ariadne_jwt.decorators import login_required
from app.models import Account, Budget, Transaction, Category


@login_required
def resolve_createAccount(
    _, info, account_name, account_type, account_balance, currency_code
):

    request = info.context["request"]

    owner = Profile.objects.get(user__id=request.user.id)

    new_account = Account.objects.create(
        account_name=account_name,
        account_type=account_type,
        account_balance=account_balance,
        currency_code=currency_code,
        owner=owner,
    )

    return new_account


@login_required
def resolve_updateAccount(
    *_, id, account_name, account_type, account_balance, currency_code
):

    account = Account.objects.get(id=id)

    account.account_name = account_name
    account.account_type = account_type
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
    budget_name,
    budget_description,
    budget_start_date,
    budget_end_date,
    budget_amount,
    category,
):

    request = info.context["request"]

    profile = Profile.objects.get(id=request.user.id)

    budget_category = Category.objects.filter(
        Q(category_name__icontains=category)
    ).first()

    start_date_object = datetime.strptime(budget_start_date, "%Y-%m-%d").date()
    end_date_object = datetime.strptime(budget_end_date, "%Y-%m-%d").date()

    start_date = set_date.date(
        start_date_object.year, start_date_object.month, start_date_object.day
    )
    end_date = set_date.date(
        end_date_object.year, end_date_object.month, end_date_object.day
    )

    new_budget = Budget.objects.create(
        budget_name=budget_name,
        budget_description=budget_description,
        budget_amount=budget_amount,
        budget_start_date=start_date,
        budget_end_date=end_date,
        category=budget_category,
        owner=profile,
    )

    return new_budget


@login_required
def resolve_updateBudget(
    *_,
    id,
    budget_name,
    budget_description,
    budget_start_date,
    budget_end_date,
    budget_amount,
    category
):

    budget = Budget.objects.get(id=id)

    budget_category = Category.objects.filter(
        Q(category_name__icontains=category)
    ).first()

    budget.budget_name = budget_name
    budget.budget_description = budget_description
    budget.budget_start_date = budget_start_date
    budget.budget_end_date = budget_end_date
    budget.budget_amount = budget_amount
    budget.category = budget_category  # type: ignore

    budget.save()

    return budget


@login_required
def resolve_deleteBudget(*_, id):

    try:

        Budget.objects.get(id=id).delete()

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
        Q(category_name__icontains=category)
    ).first()

    new_transaction = Transaction.objects.create(
        transaction_type=transaction_type,
        transaction_amount=transaction_amount,
        transaction_date=transaction_date,
        currency_code=currency_code,
        description=description,
        category=transaction_category,
        account=account,
    )

    return new_transaction


@login_required
def resolve_updateTransaction(
    *_,
    id,
    transaction_type,
    transaction_amount,
    transaction_date,
    currency_code,
    description,
    category
):

    transaction = Transaction.objects.get(id=id)

    transaction_category = Category.objects.filter(
        Q(category_name__icontains=category)
    ).first()

    transaction.transaction_type = transaction_type
    transaction.transaction_amount = transaction_amount
    transaction.transaction_date = transaction_date
    transaction.currency_code = currency_code
    transaction.description = description
    transaction.category = transaction_category  # type: ignore

    transaction.save()


@login_required
def resolve_deleteTransaction(*_, id):

    try:

        Transaction.objects.get(id=id).delete()

    except Exception as e:

        raise Exception(str(e))

    else:

        return True
