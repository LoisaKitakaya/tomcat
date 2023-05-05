from ariadne_jwt.decorators import login_required
from transactions.models import (
    Transaction,
    TransactionType,
    TransactionCategory,
    TransactionSubCategory,
)


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


@login_required
def resolve_getAllTransactions(*_, account_id):
    try:
        transactions = Transaction.objects.filter(account__id=account_id).all()

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
