from datetime import datetime
from users.models import Profile
from django.utils import timezone
from teams.models import Workspace, TeamLogs
from app.decorators import check_plan_standard
from users.limit import (
    check_create_account_limit,
    check_create_budget_limit,
    check_create_target_limit,
)
from ariadne_jwt.decorators import login_required
from app.models import (
    Account,
    Budget,
    Target,
    Product,
    Employee,
    Transaction,
    TransactionType,
    TransactionCategory,
    TransactionSubCategory,
    ProductCategory,
    ProductSubCategory,
)


@login_required
def resolve_createAccount(
    _,
    info,
    account_name,
    account_type,
    account_balance,
    currency_code,
):
    request = info.context["request"]

    check_create_account_limit(request.user.id)

    profile = Profile.objects.get(user__id=request.user.id)

    workspace = Workspace.objects.get(workspace_uid=profile.workspace_uid)

    new_account = Account.objects.create(
        account_name=account_name,
        account_type=account_type,
        account_balance=account_balance,
        currency_code=currency_code,
        owner=profile,
        workspace=workspace,
    )

    if profile.is_employee:
        TeamLogs.objects.create(
            workspace=workspace,
            user=request.user,
            action=f"Created account: {new_account.account_name}",
        )

    return new_account


@login_required
def resolve_updateAccount(
    _,
    info,
    id,
    account_name,
    account_type,
    account_balance,
    currency_code,
):
    request = info.context["request"]

    profile = Profile.objects.get(user=request.user)

    workspace = Workspace.objects.get(workspace_uid=profile.workspace_uid)

    account = Account.objects.get(id=id)

    account.account_name = account_name
    account.account_type = account_type
    account.account_balance = account_balance
    account.currency_code = currency_code

    account.save()

    if profile.is_employee:
        TeamLogs.objects.create(
            workspace=workspace,
            user=request.user,
            action=f"Updated account: {account.account_name}",
        )

    return account


@login_required
def resolve_deleteAccount(_, info, id):
    request = info.context["request"]

    profile = Profile.objects.get(user=request.user)

    workspace = Workspace.objects.get(workspace_uid=profile.workspace_uid)

    try:
        account = Account.objects.get(id=id)

        account_name = account.account_name

        account.delete()

    except Exception as e:
        raise Exception(str(e))

    if profile.is_employee:
        TeamLogs.objects.create(
            workspace=workspace,
            user=request.user,
            action=f"Deleted account: {account_name}",
        )

    return True


@login_required
def resolve_createBudget(
    _,
    info,
    account_id,
    budget_name,
    budget_description,
    budget_amount,
    category,
    sub_category,
):
    request = info.context["request"]

    check_create_budget_limit(request.user.id)

    profile = Profile.objects.get(user__id=request.user.id)

    workspace = Workspace.objects.get(workspace_uid=profile.workspace_uid)

    account = Account.objects.get(id=account_id)

    budget_category = TransactionCategory.objects.get(category_name=category)
    budget_sub_category = TransactionSubCategory.objects.get(category_name=sub_category)

    new_budget = Budget.objects.create(
        budget_name=budget_name,
        budget_description=budget_description,
        budget_amount=budget_amount,
        category=budget_category,
        sub_category=budget_sub_category,
        owner=profile,
        account=account,
        workspace=workspace,
    )

    if profile.is_employee:
        TeamLogs.objects.create(
            workspace=workspace,
            user=request.user,
            action=f"Created budget: {new_budget.budget_name}",
        )

    return new_budget


@login_required
def resolve_updateBudget(
    _,
    info,
    id,
    budget_name,
    budget_description,
    budget_amount,
    category,
    sub_category,
):
    request = info.context["request"]

    profile = Profile.objects.get(user__id=request.user.id)

    workspace = Workspace.objects.get(workspace_uid=profile.workspace_uid)

    budget = Budget.objects.get(id=id)

    budget_category = TransactionCategory.objects.get(category_name=category)
    budget_sub_category = TransactionSubCategory.objects.get(category_name=sub_category)

    budget.budget_name = budget_name
    budget.budget_description = budget_description
    budget.budget_amount = budget_amount
    budget.category = budget_category
    budget.sub_category = budget_sub_category

    budget.save()

    if profile.is_employee:
        TeamLogs.objects.create(
            workspace=workspace,
            user=request.user,
            action=f"Updated budget: {budget.budget_name}",
        )

    return budget


@login_required
def resolve_budgetStatus(_, info, id, status):
    request = info.context["request"]

    profile = Profile.objects.get(user__id=request.user.id)

    workspace = Workspace.objects.get(workspace_uid=profile.workspace_uid)

    budget = Budget.objects.get(id=id)

    budget.budget_is_active = status

    budget.save()

    if profile.is_employee:
        TeamLogs.objects.create(
            workspace=workspace,
            user=request.user,
            action=f"Updated budget status to: {status}",
        )

    return True


@login_required
def resolve_deleteBudget(_, info, id):
    request = info.context["request"]

    profile = Profile.objects.get(user__id=request.user.id)

    workspace = Workspace.objects.get(workspace_uid=profile.workspace_uid)

    try:
        budget = Budget.objects.get(id=id)

        budget_name = budget.budget_name

        budget.delete()

    except Exception as e:
        raise Exception(str(e))

    if profile.is_employee:
        TeamLogs.objects.create(
            workspace=workspace,
            user=request.user,
            action=f"Deleted budget: {budget_name}",
        )

    return True


@login_required
def resolve_createTarget(
    _,
    info,
    account_id,
    target_name,
    target_description,
    target_amount,
    category,
    sub_category,
):
    request = info.context["request"]

    check_create_target_limit(request.user.id)

    profile = Profile.objects.get(user__id=request.user.id)

    workspace = Workspace.objects.get(workspace_uid=profile.workspace_uid)

    account = Account.objects.get(id=account_id)

    target_category = TransactionCategory.objects.get(category_name=category)
    target_sub_category = TransactionSubCategory.objects.get(category_name=sub_category)

    new_target = Target.objects.create(
        target_name=target_name,
        target_description=target_description,
        target_amount=target_amount,
        category=target_category,
        sub_category=target_sub_category,
        owner=profile,
        account=account,
        workspace=workspace,
    )

    if profile.is_employee:
        TeamLogs.objects.create(
            workspace=workspace,
            user=request.user,
            action=f"Created target: {new_target.target_name}",
        )

    return new_target


@login_required
def resolve_updateTarget(
    _,
    info,
    id,
    target_name,
    target_description,
    target_amount,
    category,
    sub_category,
):
    request = info.context["request"]

    profile = Profile.objects.get(user__id=request.user.id)

    workspace = Workspace.objects.get(workspace_uid=profile.workspace_uid)

    target = Target.objects.get(id=id)

    target_category = TransactionCategory.objects.get(category_name=category)
    target_sub_category = TransactionSubCategory.objects.get(category_name=sub_category)

    target.target_name = target_name
    target.target_description = target_description
    target.target_amount = target_amount
    target.category = target_category
    target.sub_category = target_sub_category

    target.save()

    if profile.is_employee:
        TeamLogs.objects.create(
            workspace=workspace,
            user=request.user,
            action=f"Updated target: {target.target_name}",
        )

    return target


@login_required
def resolve_targetStatus(_, info, id, status):
    request = info.context["request"]

    profile = Profile.objects.get(user__id=request.user.id)

    workspace = Workspace.objects.get(workspace_uid=profile.workspace_uid)

    target = Target.objects.get(id=id)

    target.target_is_active = status

    target.save()

    if profile.is_employee:
        TeamLogs.objects.create(
            workspace=workspace,
            user=request.user,
            action=f"Updated target status to: {status}",
        )

    return True


@login_required
def resolve_deleteTarget(_, info, id):
    request = info.context["request"]

    profile = Profile.objects.get(user__id=request.user.id)

    workspace = Workspace.objects.get(workspace_uid=profile.workspace_uid)

    try:
        target = Target.objects.get(id=id)

        target_name = target.target_name

        target.delete()

    except Exception as e:
        raise Exception(str(e))

    if profile.is_employee:
        TeamLogs.objects.create(
            workspace=workspace,
            user=request.user,
            action=f"Deleted target: {target_name}",
        )

    return True


@login_required
def resolve_createTransaction(
    _,
    info,
    account_id,
    transaction_type,
    transaction_amount,
    transaction_date,
    description,
    category,
    sub_category,
):
    request = info.context["request"]

    profile = Profile.objects.get(user__id=request.user.id)

    workspace = Workspace.objects.get(workspace_uid=profile.workspace_uid)

    account = Account.objects.get(id=account_id)

    type = TransactionType.objects.get(type_name=transaction_type)

    transaction_category = TransactionCategory.objects.get(category_name=category)
    transaction_sub_category = TransactionSubCategory.objects.get(
        category_name=sub_category
    )

    date_object = datetime.strptime(transaction_date, "%Y-%m-%dT%H:%M")
    new_date_object = timezone.make_aware(date_object)

    new_transaction = Transaction.objects.create(
        transaction_type=type,
        transaction_amount=transaction_amount,
        transaction_date=new_date_object,
        currency_code=account.currency_code,
        description=description,
        category=transaction_category,
        sub_category=transaction_sub_category,
        account=account,
    )

    if transaction_type == "payable":
        account.account_balance -= transaction_amount

        account.save()

    elif transaction_type == "receivable":
        account.account_balance += transaction_amount

        account.save()

    if profile.is_employee:
        TeamLogs.objects.create(
            workspace=workspace,
            user=request.user,
            action=f"Created transaction of ID: {new_transaction.pk}, \
                in account: {account.account_name}",
        )

    return new_transaction


@login_required
def resolve_updateTransaction(
    _,
    info,
    id,
    account_id,
    transaction_type,
    transaction_amount,
    transaction_date,
    description,
    category,
    sub_category,
):
    request = info.context["request"]

    profile = Profile.objects.get(user__id=request.user.id)

    workspace = Workspace.objects.get(workspace_uid=profile.workspace_uid)

    account = Account.objects.get(id=account_id)

    transaction = Transaction.objects.get(id=id)

    type = TransactionType.objects.get(type_name=transaction_type)

    transaction_category = TransactionCategory.objects.get(category_name=category)
    transaction_sub_category = TransactionSubCategory.objects.get(
        category_name=sub_category
    )

    date_object = datetime.strptime(transaction_date, "%Y-%m-%dT%H:%M")
    new_date_object = timezone.make_aware(date_object)

    if (
        transaction_type == "payable"
        and transaction.transaction_type.type_name == "payable"
    ):
        previous_balance = account.account_balance + transaction.transaction_amount

        account.account_balance = previous_balance - transaction_amount

        account.save()

    elif (
        transaction_type == "receivable"
        and transaction.transaction_type.type_name == "receivable"
    ):
        previous_balance = account.account_balance - transaction.transaction_amount

        account.account_balance = previous_balance + transaction_amount

        account.save()

    elif (
        transaction_type == "payable"
        and transaction.transaction_type.type_name == "receivable"
    ):
        previous_balance = account.account_balance - transaction.transaction_amount

        account.account_balance = previous_balance - transaction_amount

        account.save()

    elif (
        transaction_type == "receivable"
        and transaction.transaction_type.type_name == "payable"
    ):
        previous_balance = account.account_balance + transaction.transaction_amount

        account.account_balance = previous_balance + transaction_amount

        account.save()

    transaction.transaction_type = type
    transaction.transaction_amount = transaction_amount
    transaction.transaction_date = new_date_object
    transaction.description = description
    transaction.category = transaction_category
    transaction.sub_category = transaction_sub_category

    transaction.save()

    if profile.is_employee:
        TeamLogs.objects.create(
            workspace=workspace,
            user=request.user,
            action=f"Created transaction of ID: {transaction.pk}, \
                in account: {account.account_name}",
        )

    return transaction


@login_required
def resolve_deleteTransaction(_, info, id, account_id):
    request = info.context["request"]

    profile = Profile.objects.get(user__id=request.user.id)

    workspace = Workspace.objects.get(workspace_uid=profile.workspace_uid)

    account = Account.objects.get(id=account_id)

    transaction = Transaction.objects.get(id=id)

    if transaction.transaction_type == "payable":
        previous_balance = account.account_balance + transaction.transaction_amount

        account.account_balance = previous_balance

        account.save()

    elif transaction.transaction_type == "receivable":
        previous_balance = account.account_balance - transaction.transaction_amount

        account.account_balance = previous_balance

        account.save()

    transaction.delete()

    if profile.is_employee:
        TeamLogs.objects.create(
            workspace=workspace,
            user=request.user,
            action=f"Deleted transaction of ID: {transaction.pk}, \
                in account: {account.account_name}",
        )

    return True


@login_required
@check_plan_standard
def resolve_createEmployee(
    _,
    info,
    account_id,
    email,
    first_name,
    last_name,
    phone_number,
    ID_number,
    employment_status,
    job_title,
    job_description,
    is_manager,
    salary,
    department,
    employee_id,
    emergency_contact_name,
    emergency_contact_phone_number,
    emergency_contact_email,
    date_of_hire,
):
    request = info.context["request"]

    profile = Profile.objects.get(user__id=request.user.id)

    workspace = Workspace.objects.get(workspace_uid=profile.workspace_uid)

    account = Account.objects.get(id=account_id)

    date_object = datetime.strptime(date_of_hire, "%Y-%m-%d")
    new_date_object = timezone.make_aware(date_object)

    employee = Employee.objects.create(
        account=account,
        workspace=workspace,
        email=email,
        first_name=first_name,
        last_name=last_name,
        phone_number=phone_number,
        ID_number=ID_number,
        employment_status=employment_status,
        job_title=job_title,
        job_description=job_description,
        is_manager=is_manager,
        salary=salary,
        department=department,
        employee_id=employee_id,
        emergency_contact_name=emergency_contact_name,
        emergency_contact_phone_number=emergency_contact_phone_number,
        emergency_contact_email=emergency_contact_email,
        date_of_hire=new_date_object,
    )

    if profile.is_employee:
        TeamLogs.objects.create(
            workspace=workspace,
            user=request.user,
            action=f"Created employee: {employee.first_name} {employee.last_name}",
        )

    return employee


@login_required
@check_plan_standard
def resolve_updateEmployee(
    _,
    info,
    id,
    email,
    first_name,
    last_name,
    phone_number,
    ID_number,
    employment_status,
    job_title,
    job_description,
    is_manager,
    salary,
    department,
    employee_id,
    emergency_contact_name,
    emergency_contact_phone_number,
    emergency_contact_email,
    date_of_hire,
):
    request = info.context["request"]

    profile = Profile.objects.get(user__id=request.user.id)

    workspace = Workspace.objects.get(workspace_uid=profile.workspace_uid)

    employee = Employee.objects.get(id=id)

    new_date_object = employee.date_of_hire

    if date_of_hire:
        date_object = datetime.strptime(date_of_hire, "%Y-%m-%d")
        new_date_object = timezone.make_aware(date_object)

    employee.email = email if email else employee.email
    employee.first_name = first_name if first_name else employee.first_name
    employee.last_name = last_name if last_name else employee.last_name
    employee.phone_number = phone_number if phone_number else employee.phone_number
    employee.ID_number = ID_number if ID_number else employee.ID_number
    employee.employment_status = (
        employment_status if employment_status else employee.employment_status
    )
    employee.job_title = job_title if job_title else employee.job_title
    employee.job_description = (
        job_description if job_description else employee.job_description
    )
    employee.is_manager = is_manager if is_manager else employee.is_manager
    employee.salary = salary if salary else employee.salary
    employee.department = department if department else employee.department
    employee.employee_id = employee_id if employee_id else employee.employee_id
    employee.emergency_contact_name = (
        emergency_contact_name
        if emergency_contact_name
        else employee.emergency_contact_name
    )
    employee.emergency_contact_phone_number = (
        emergency_contact_phone_number
        if emergency_contact_phone_number
        else employee.emergency_contact_phone_number
    )
    employee.emergency_contact_email = (
        emergency_contact_email
        if emergency_contact_email
        else employee.emergency_contact_email
    )
    employee.date_of_hire = new_date_object

    employee.save()

    if profile.is_employee:
        TeamLogs.objects.create(
            workspace=workspace,
            user=request.user,
            action=f"Updated employee: {employee.first_name} {employee.last_name}",
        )

    return employee


@login_required
@check_plan_standard
def resolve_deleteEmployee(_, info, id):
    request = info.context["request"]

    profile = Profile.objects.get(user__id=request.user.id)

    workspace = Workspace.objects.get(workspace_uid=profile.workspace_uid)

    try:
        employee = Employee.objects.get(id=id)

        employee_name = f"{employee.first_name} {employee.last_name}"

        employee.delete()

    except Exception as e:
        raise Exception(str(e))

    if profile.is_employee:
        TeamLogs.objects.create(
            workspace=workspace,
            user=request.user,
            action=f"Deleted employee: {employee_name}",
        )

    return True


@login_required
@check_plan_standard
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
@check_plan_standard
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
@check_plan_standard
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
