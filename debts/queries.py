from accounts.models import Account
from debts.models import Customer, Debt
from ariadne_jwt.decorators import login_required


@login_required
def resolve_getAllCustomers(*_, account_id):
    account = Account.objects.get(id=account_id)

    customer = Customer.objects.filter(account__id=account.pk).all()

    return customer


@login_required
def resolve_getCustomer(*_, id):
    try:
        customer = Customer.objects.get(id=id)

    except Exception as e:
        raise Exception(str(e))

    return customer


@login_required
def resolve_getAllDebts(*_, account_id):
    account = Account.objects.get(id=account_id)

    debt = Debt.objects.filter(account__id=account.pk).all()

    return debt


@login_required
def resolve_getDebt(*_, id):
    try:
        debt = Debt.objects.get(id=id)

    except Exception as e:
        raise Exception(str(e))

    return debt
