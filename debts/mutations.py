from datetime import datetime
from users.models import Profile
from django.utils import timezone
from accounts.models import Account
from debts.models import Customer, Debt
from teams.models import Workspace, TeamLogs
from ariadne_jwt.decorators import login_required


@login_required
def resolve_createCustomer(_, info, account_id, name, email, phone):
    request = info.context["request"]

    profile = Profile.objects.get(user__id=request.user.id)

    workspace = Workspace.objects.get(workspace_uid=profile.workspace_uid)

    account = Account.objects.get(id=account_id)

    new_customer = Customer.objects.create(
        account=account,
        name=name,
        email=email,
        phone=phone,
    )

    if profile.is_employee:
        TeamLogs.objects.create(
            workspace=workspace,
            user=request.user,
            action=f"Created new customer: {new_customer.name}",
        )

    return new_customer


@login_required
def resolve_updateCustomer(_, info, id, name, email, phone):
    request = info.context["request"]

    profile = Profile.objects.get(user__id=request.user.id)

    workspace = Workspace.objects.get(workspace_uid=profile.workspace_uid)

    customer = Customer.objects.get(id=id)

    customer.name = name or customer.name
    customer.email = email or customer.email
    customer.phone = phone or customer.phone

    customer.save()

    if profile.is_employee:
        TeamLogs.objects.create(
            workspace=workspace,
            user=request.user,
            action=f"Updated customer: {customer.name}",
        )

    return customer


@login_required
def resolve_deleteCustomer(_, info, id):
    request = info.context["request"]

    profile = Profile.objects.get(user__id=request.user.id)

    workspace = Workspace.objects.get(workspace_uid=profile.workspace_uid)

    try:
        customer = Customer.objects.get(id=id)

        customer_name = customer.name

        customer.delete()

    except Exception as e:
        raise Exception(str(e))

    if profile.is_employee:
        TeamLogs.objects.create(
            workspace=workspace,
            user=request.user,
            action=f"Deleted customer: {customer_name}",
        )

    return True


@login_required
def resolve_recordDebt(_, info, account_id, customer_id, amount, due_date):
    request = info.context["request"]

    profile = Profile.objects.get(user__id=request.user.id)

    workspace = Workspace.objects.get(workspace_uid=profile.workspace_uid)

    account = Account.objects.get(id=account_id)

    customer = Customer.objects.get(id=customer_id)

    date_object = datetime.strptime(due_date, "%Y-%m-%d")
    new_date_object = timezone.make_aware(date_object)

    debt_record = Debt.objects.create(
        account=account,
        customer=customer,
        amount=amount,
        due_date=new_date_object,
    )

    if profile.is_employee:
        TeamLogs.objects.create(
            workspace=workspace,
            user=request.user,
            action=f"Created debt record of ID: {debt_record.pk}",
        )

    return debt_record

@login_required
def resolve_updateDebt(_, info, id, amount, due_date, is_paid):
    request = info.context["request"]

    profile = Profile.objects.get(user__id=request.user.id)

    workspace = Workspace.objects.get(workspace_uid=profile.workspace_uid)

    debt = Debt.objects.get(id=id)

    date_object = datetime.strptime(due_date, "%Y-%m-%d")
    new_date_object = timezone.make_aware(date_object)

    debt.amount = amount or debt.amount
    debt.due_date = new_date_object if due_date else debt.due_date
    debt.is_paid = is_paid or debt.is_paid

    debt.save()

    if profile.is_employee:
        TeamLogs.objects.create(
            workspace=workspace,
            user=request.user,
            action=f"Updated debt record of ID: {debt.pk}",
        )

    return debt

@login_required
def resolve_deleteDebt(_, info, id):
    request = info.context["request"]

    profile = Profile.objects.get(user__id=request.user.id)

    workspace = Workspace.objects.get(workspace_uid=profile.workspace_uid)

    try:
        debt = Customer.objects.get(id=id)

        debt.delete()

    except Exception as e:
        raise Exception(str(e))

    if profile.is_employee:
        TeamLogs.objects.create(
            workspace=workspace,
            user=request.user,
            action=f"Deleted debt record of ID: {debt.pk}",
        )

    return True
