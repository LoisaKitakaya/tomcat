from users.models import Profile
from accounts.models import Account
from teams.models import Workspace, TeamLogs
from ariadne_jwt.decorators import login_required
from inventory.models import Product, ProductCategory, ProductSubCategory


@login_required
def resolve_createProduct(
    _,
    info,
    account_id,
    name,
    description,
    category,
    sub_category,
    buying_price,
    selling_price,
    current_stock_level,
    units_sold,
    reorder_level,
    supplier_name,
    supplier_phone_number,
    supplier_email,
):
    request = info.context["request"]

    profile = Profile.objects.get(user__id=request.user.id)

    workspace = Workspace.objects.get(workspace_uid=profile.workspace_uid)

    account = Account.objects.get(id=account_id)

    profit = (selling_price - buying_price) * units_sold

    prod_category = ProductCategory.objects.get(category_name=category)
    prod_sub_category = ProductSubCategory.objects.get(category_name=sub_category)

    product = Product.objects.create(
        account=account,
        workspace=workspace,
        name=name,
        description=description,
        category=prod_category,
        sub_category=prod_sub_category,
        buying_price=buying_price,
        selling_price=selling_price,
        current_stock_level=current_stock_level,
        units_sold=units_sold,
        reorder_level=reorder_level,
        reorder_quantity=units_sold,
        supplier_name=supplier_name,
        supplier_phone_number=supplier_phone_number,
        supplier_email=supplier_email,
        profit_generated=profit,
    )

    if profile.is_employee:
        TeamLogs.objects.create(
            workspace=workspace,
            user=request.user,
            action=f"Created product: {product.name}",
        )

    return product


@login_required
def resolve_updateProduct(
    _,
    info,
    id,
    name,
    description,
    category,
    sub_category,
    buying_price,
    selling_price,
    current_stock_level,
    units_sold,
    reorder_level,
    supplier_name,
    supplier_phone_number,
    supplier_email,
):
    request = info.context["request"]

    profile = Profile.objects.get(user__id=request.user.id)

    workspace = Workspace.objects.get(workspace_uid=profile.workspace_uid)

    product = Product.objects.get(id=id)

    profit = product.profit_generated

    if selling_price or buying_price or units_sold:
        profit = (selling_price - buying_price) * units_sold

    prod_category = ProductCategory.objects.get(category_name=category)
    prod_sub_category = ProductSubCategory.objects.get(category_name=sub_category)

    product.name = name if name else product.name
    product.description = description if description else product.description
    product.category = prod_category if category else product.category
    product.sub_category = prod_sub_category if sub_category else product.sub_category
    product.buying_price = buying_price if buying_price else product.buying_price
    product.selling_price = selling_price if selling_price else product.selling_price
    product.current_stock_level = (
        current_stock_level if current_stock_level else product.current_stock_level
    )
    product.units_sold = units_sold if units_sold else product.units_sold
    product.reorder_level = reorder_level if reorder_level else product.reorder_level
    product.reorder_quantity = units_sold if units_sold else product.reorder_quantity
    product.supplier_name = supplier_name if supplier_name else product.supplier_name
    product.supplier_phone_number = (
        supplier_phone_number
        if supplier_phone_number
        else product.supplier_phone_number
    )
    product.supplier_email = (
        supplier_email if supplier_email else product.supplier_email
    )
    product.profit_generated = profit

    product.save()

    if profile.is_employee:
        TeamLogs.objects.create(
            workspace=workspace,
            user=request.user,
            action=f"Updated product: {product.name}",
        )

    return product


@login_required
def resolve_deleteProduct(_, info, id):
    request = info.context["request"]

    profile = Profile.objects.get(user__id=request.user.id)

    workspace = Workspace.objects.get(workspace_uid=profile.workspace_uid)

    try:
        product = Product.objects.get(id=id)

        product_name = f"{product.name}"

        product.delete()

    except Exception as e:
        raise Exception(str(e))

    if profile.is_employee:
        TeamLogs.objects.create(
            workspace=workspace,
            user=request.user,
            action=f"Deleted product: {product_name}",
        )

    return True
