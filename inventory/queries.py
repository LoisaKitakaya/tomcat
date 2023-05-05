from accounts.models import Account
from inventory.models import Product
from ariadne_jwt.decorators import login_required


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
