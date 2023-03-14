from ariadne_jwt.decorators import login_required
from app.models import Account, Category, Budget, Transaction, Report

# Category model query resolvers


@login_required
def resolve_getAllCategories(*_):

    try:

        categories = Category.objects.all()

    except Exception as e:

        raise Exception(str(e))

    return categories


@login_required
def resolve_getCategoryByPublicId(*_, public_id):

    try:

        category = Category.objects.filter(public_id=public_id).first()

    except Exception as e:

        raise Exception(str(e))

    return category


# Account model query resolvers


@login_required
def resolve_getAllAccounts(*_):

    try:

        accounts = Account.objects.all()

    except Exception as e:

        raise Exception(str(e))

    return accounts


@login_required
def resolve_getAccount(_, info):

    request = info.context["request"]

    try:

        account = Account.objects.get(public_id=request.user.public_id)

    except Exception as e:

        raise Exception(str(e))

    return account


# Budget model query resolvers


@login_required
def resolve_getAllBudgets(*_):

    try:

        budgets = Budget.objects.all()

    except Exception as e:

        raise Exception(str(e))

    return budgets


@login_required
def resolve_getBudget(*_, info):

    request = info.context["request"]

    try:

        budget = Budget.objects.filter(public_id=request.user.public_id).first()

    except Exception as e:

        raise Exception(str(e))

    return budget


# Transaction model query resolvers


@login_required
def resolve_getAllTransactions(*_):

    try:

        transactions = Transaction.objects.all()

    except Exception as e:

        raise Exception(str(e))

    return transactions


@login_required
def resolve_getTransaction(_, info):

    request = info.context["request"]

    try:

        transaction = Transaction.objects.filter(
            public_id=request.user.public_id
        ).first()

    except Exception as e:

        raise Exception(str(e))

    return transaction


# Report model query resolvers


@login_required
def resolve_getAllReports(*_):

    try:

        reports = Report.objects.all()

    except Exception as e:

        raise Exception(str(e))

    return reports


@login_required
def resolve_getReport(_, info):

    request = info.context["request"]

    try:

        report = Report.objects.get(public_id=request.user.public_id)

    except Exception as e:

        raise Exception(str(e))

    return report
