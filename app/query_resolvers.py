from users.models import Profile
from app.models import Account, Category, Budget, Transaction, Report

# Category model query resolvers


def resolve_getAllCategories(*_):

    try:

        categories = Category.objects.all()

    except Exception as e:

        raise Exception(str(e))

    return categories


def resolve_getCategoryByPublicId(*_, public_id):

    try:

        category = Category.objects.filter(public_id=public_id).first()

    except Exception as e:

        raise Exception(str(e))

    return category


# Account model query resolvers


def resolve_getAllAccounts(*_):

    try:

        accounts = Account.objects.all()

    except Exception as e:

        raise Exception(str(e))

    return accounts


def resolve_getAccountByPublicId(*_, public_id):

    try:

        account = Account.objects.get(public_id=public_id)

    except Exception as e:

        raise Exception(str(e))

    return account


def resolve_getAccountByProfilePublicId(*_, public_id):

    try:

        profile = Profile.objects.get(public_id=public_id)

        accounts = Account.objects.filter(profile__public_id=profile.public_id).all()

    except Exception as e:

        raise Exception(str(e))

    return accounts


# Budget model query resolvers


def resolve_getAllBudgets(*_):

    try:

        budgets = Budget.objects.all()

    except Exception as e:

        raise Exception(str(e))

    return budgets


def resolve_getBudgetByPublicId(*_, public_id):

    try:

        budget = Budget.objects.filter(public_id=public_id).first()

    except Exception as e:

        raise Exception(str(e))

    return budget


def resolve_getBudgetByProfilePublicId(*_, public_id):

    try:

        profile = Profile.objects.get(public_id=public_id)

        budgets = Budget.objects.filter(profile__public_id=profile.public_id).all()

    except Exception as e:

        raise Exception(str(e))

    return budgets


def resolve_getBudgetByCategoryPublicId(*_, public_id):

    try:

        category = Category.objects.get(public_id=public_id)

        budgets = Budget.objects.filter(category__public_id=category.public_id).all()

    except Exception as e:

        raise Exception(str(e))

    return budgets


# Transaction model query resolvers


def resolve_getAllTransactions(*_):

    try:

        transactions = Transaction.objects.all()

    except Exception as e:

        raise Exception(str(e))

    return transactions


def resolve_getTransactionByPublicId(*_, public_id):

    try:

        transaction = Transaction.objects.get(public_id=public_id)

    except Exception as e:

        raise Exception(str(e))

    return transaction


def resolve_getTransactionByAccountPublicId(*_, public_id):

    try:

        account = Account.objects.get(public_id=public_id)

        transactions = Transaction.objects.filter(
            account__public_id=account.public_id
        ).all()

    except Exception as e:

        raise Exception(str(e))

    return transactions


def resolve_getTransactionByCategoryPublicId(*_, public_id):

    try:

        category = Category.objects.get(public_id=public_id)

        transactions = Transaction.objects.filter(
            category__public_id=category.public_id
        ).all()

    except Exception as e:

        raise Exception(str(e))

    return transactions


# Report model query resolvers


def resolve_getAllReports(*_):

    try:

        reports = Report.objects.all()

    except Exception as e:

        raise Exception(str(e))

    return reports


def resolve_getReportByPublicId(*_, public_id):

    try:

        report = Report.objects.get(public_id=public_id)

    except Exception as e:

        raise Exception(str(e))

    return report


def resolve_getReportByAccountPublicId(*_, public_id):

    try:

        account = Account.objects.get(public_id=public_id)

        reports = Report.objects.filter(account__public_id=account.public_id).all()

    except Exception as e:

        raise Exception(str(e))

    return reports


def resolve_getReportByCategoryPublicId(*_, public_id):

    try:

        category = Category.objects.get(public_id=public_id)

        reports = Report.objects.filter(category__public_id=category.public_id).all()

    except Exception as e:

        raise Exception(str(e))

    return reports
