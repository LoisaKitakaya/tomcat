from users.models import Profile
from teams.models import Workspace
from ariadne_jwt.decorators import login_required
from app.models import Account, Budget, Transaction, Target


# Account model query resolvers


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
