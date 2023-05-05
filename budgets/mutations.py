from users.models import Profile
from budgets.models import Budget
from accounts.models import Account
from teams.models import Workspace, TeamLogs
from ariadne_jwt.decorators import login_required
from transactions.models import TransactionCategory, TransactionSubCategory


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
