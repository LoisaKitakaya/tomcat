from accounts.models import Account
from ariadne_jwt.decorators import login_required
from inventory.models import Product, ProductCategory, ProductSubCategory


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
