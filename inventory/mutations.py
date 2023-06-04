from users.models import Profile
from accounts.models import Account
from teams.models import Workspace, TeamLogs
from ariadne_jwt.decorators import login_required
from inventory.models import Product, ProductCategory, ProductSubCategory


@login_required
def resolve_createProduct(
    *_,
    account_id,
    name: str,
    description: str,
    category: str,
    sub_category: str,
    buying_price: str,
    selling_price: str,
    current_stock_level: str,
    units_sold: str,
    supplier_name: str,
    supplier_phone_number: str,
    supplier_email: str,
):
    account = Account.objects.get(id=account_id)

    profit = (float(selling_price) - float(buying_price)) * int(units_sold)

    prod_category = ProductCategory.objects.get(category_name=category)
    prod_sub_category = ProductSubCategory.objects.get(category_name=sub_category)

    product = Product.objects.create(
        account=account,
        name=name,
        description=description,
        category=prod_category,
        sub_category=prod_sub_category,
        buying_price=float(buying_price),
        selling_price=float(selling_price),
        current_stock_level=int(current_stock_level),
        units_sold=int(units_sold),
        profit_generated=profit,
        supplier_name=supplier_name,
        supplier_phone_number=supplier_phone_number,
        supplier_email=supplier_email,
    )

    return product


@login_required
def resolve_updateProduct(
    *_,
    id,
    name: str,
    description: str,
    category: str,
    sub_category: str,
    buying_price: str,
    selling_price: str,
    current_stock_level: str,
    units_sold: str,
    supplier_name: str,
    supplier_phone_number: str,
    supplier_email: str,
):
    product = Product.objects.get(id=id)

    if selling_price or buying_price or units_sold:
        profit = (
            (
                (float(selling_price) if selling_price else product.selling_price)
                - (float(buying_price) if buying_price else product.buying_price)
            )
            * int(units_sold)
            if units_sold
            else product.units_sold
        )

    else:
        profit = product.profit_generated

    if units_sold:
        stock = (
            int(current_stock_level)
            if current_stock_level
            else product.current_stock_level - int(units_sold)
        )

    else:
        stock = product.current_stock_level

    prod_category = (
        ProductCategory.objects.get(category_name=category)
        if category
        else product.category
    )

    prod_sub_category = (
        ProductSubCategory.objects.get(category_name=sub_category)
        if sub_category
        else product.sub_category
    )

    product.name = name if name else product.name
    product.description = description if description else product.description
    product.category = prod_category
    product.sub_category = prod_sub_category
    product.buying_price = float(buying_price) if buying_price else product.buying_price
    product.selling_price = (
        float(selling_price) if selling_price else product.selling_price
    )
    product.current_stock_level = stock
    product.units_sold = int(units_sold) if units_sold else product.units_sold
    product.profit_generated = profit
    product.supplier_name = supplier_name if supplier_name else product.supplier_name
    product.supplier_phone_number = (
        supplier_phone_number
        if supplier_phone_number
        else product.supplier_phone_number
    )
    product.supplier_email = (
        supplier_email if supplier_email else product.supplier_email
    )

    product.save()

    return product


@login_required
def resolve_deleteProduct(*_, id):
    try:
        product = Product.objects.get(id=id)

        product.delete()

    except Exception as e:
        raise Exception(str(e))

    return True
