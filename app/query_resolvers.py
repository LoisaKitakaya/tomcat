from billing.models import Plan
from users.models import Profile
from users.models import Profile
from teams.models import Workspace
from ariadne_jwt.decorators import login_required
from controls.decorators import check_plan_standard, check_plan_pro, check_is_employee
from app.models import (
    Budget,
    Target,
    Product,
    Account,
    Employee,
    Transaction,
    ProductCategory,
    TransactionType,
    ProductSubCategory,
    TransactionCategory,
    TransactionSubCategory,
)


# Account model query resolvers
def resolve_getTransactionType(*_):
    try:
        types = TransactionType.objects.all()

    except Exception as e:
        raise Exception(str(e))

    return types


def resolve_getTransactionCategory(*_):
    try:
        categories = TransactionCategory.objects.all()

    except Exception as e:
        raise Exception(str(e))

    return categories


def resolve_getTransactionSubCategory(*_, parent):
    try:
        sub_categories = TransactionSubCategory.objects.filter(
            parent__category_name=parent
        ).all()

    except Exception as e:
        raise Exception(str(e))

    return sub_categories


def resolve_getProductCategory(*_):
    try:
        categories = ProductCategory.objects.all()

    except Exception as e:
        raise Exception(str(e))

    return categories


def resolve_getProductSubCategory(*_, parent):
    try:
        sub_categories = ProductSubCategory.objects.filter(
            parent__category_name=parent
        ).all()

    except Exception as e:
        raise Exception(str(e))

    return sub_categories


@login_required
def resolve_getAllAccounts(_, info):
    request = info.context["request"]

    profile = Profile.objects.get(user__id=request.user.id)

    workspace = Workspace.objects.get(workspace_uid=profile.workspace_uid)

    accounts = Account.objects.filter(workspace__id=workspace.pk).all()

    return accounts


@login_required
def resolve_getAccount(*_, id):
    try:
        account = Account.objects.get(id=id)

    except Exception as e:
        raise Exception(str(e))

    return account


# Budget model query resolvers


@login_required
def resolve_getAllBudgets(_, info):
    request = info.context["request"]

    profile = Profile.objects.get(user__id=request.user.id)

    workspace = Workspace.objects.get(workspace_uid=profile.workspace_uid)

    budgets = Budget.objects.filter(workspace__id=workspace.pk).all()

    return budgets


@login_required
def resolve_getBudget(*_, id):
    try:
        budget = Budget.objects.get(id=id)

    except Exception as e:
        raise Exception(str(e))

    return budget


@login_required
def resolve_getAllTargets(_, info):
    request = info.context["request"]

    profile = Profile.objects.get(user__id=request.user.id)

    workspace = Workspace.objects.get(workspace_uid=profile.workspace_uid)

    targets = Target.objects.filter(workspace__id=workspace.pk).all()

    return targets


@login_required
def resolve_getTarget(*_, id):
    try:
        target = Target.objects.get(id=id)

    except Exception as e:
        raise Exception(str(e))

    return target


# Transaction model query resolvers


@login_required
def resolve_getAllTransactions(*_, id):
    try:
        transactions = Transaction.objects.filter(account__id=id).all()

    except Exception as e:
        raise Exception(str(e))

    return transactions


@login_required
def resolve_getTransaction(*_, id):
    try:
        transaction = Transaction.objects.get(id=id)

    except Exception as e:
        raise Exception(str(e))

    return transaction


@login_required
def resolve_getAllEmployees(*_, account_id):
    account = Account.objects.get(id=account_id)

    employees = Employee.objects.filter(account__id=account.pk).all()

    return employees


@login_required
def resolve_getEmployee(*_, id):
    try:
        employee = Employee.objects.get(id=id)

    except Exception as e:
        raise Exception(str(e))

    return employee


@login_required
def resolve_getAllProducts(*_, account_id):
    account = Account.objects.get(id=account_id)

    product = Product.objects.filter(account_id=account.pk).all()

    return product


@login_required
def resolve_getProduct(*_, id):
    try:
        product = Product.objects.get(id=id)

    except Exception as e:
        raise Exception(str(e))

    return product


@login_required
@check_plan_standard
def resolve_testStandardDecorator(_, info):
    request = info.context["request"]

    profile = Profile.objects.get(user__id=request.user.id)

    plan = Plan.objects.get(name=profile.Plan.name)

    return plan


@login_required
@check_plan_pro
def resolve_testProDecorator(_, info):
    request = info.context["request"]

    profile = Profile.objects.get(user__id=request.user.id)

    plan = Plan.objects.get(name=profile.Plan.name)

    return plan


@login_required
@check_is_employee
def resolve_testIfIsEmployee(_, info):
    request = info.context["request"]

    profile = Profile.objects.get(user__id=request.user.id)

    assert profile.user.pk == request.user.id

    return True
