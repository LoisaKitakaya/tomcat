import time
from users.models import Profile
from ariadne_jwt.decorators import login_required
from app.models import Account, Category, Budget, Transaction

# Category model query resolvers


@login_required
def resolve_getAllCategories(*_):

    try:

        categories = Category.objects.all()

    except Exception as e:

        raise Exception(str(e))

    return categories


@login_required
def resolve_getCategoryByPublicId(*_, id):

    try:

        category = Category.objects.filter(id=id).first()

    except Exception as e:

        raise Exception(str(e))

    return category


# Account model query resolvers


@login_required
def resolve_getAllAccounts(_, info):

    request = info.context["request"]

    try:

        profile = Profile.objects.get(user__id=request.user.id)

        accounts = Account.objects.filter(owner__id=profile.pk).all()

    except Exception as e:

        raise Exception(str(e))

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

    try:

        profile = Profile.objects.get(user__id=request.user.id)

        budgets = Budget.objects.filter(owner__id=profile.pk).all()

    except Exception as e:

        raise Exception(str(e))

    return budgets


@login_required
def resolve_getBudget(*_, id):

    try:

        budget = Budget.objects.get(id=id)

    except Exception as e:

        raise Exception(str(e))

    return budget


# Transaction model query resolvers


@login_required
def resolve_getAllTransactions(*_, id):

    try:

        transactions = Transaction.objects.filter(account__id=id).all()

    except Exception as e:

        raise Exception(str(e))

    return transactions


@login_required
def resolve_getTransactionsByAccount(*_, id):

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
