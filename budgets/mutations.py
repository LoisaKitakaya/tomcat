from users.models import Profile
from budgets.models import Budget
from accounts.models import Account
from ariadne_jwt.decorators import login_required
from transactions.models import TransactionCategory, TransactionSubCategory


@login_required
def resolve_createBudget(
    _,
    info,
    account_id,
    budget_name: str,
    budget_description: str,
    budget_amount: str,
    category: str,
    sub_category: str,
):
    request = info.context["request"]

    profile = Profile.objects.get(user__id=request.user.id)  # type: ignore

    account = Account.objects.get(id=account_id)

    budget_category = TransactionCategory.objects.get(category_name=category)
    budget_sub_category = TransactionSubCategory.objects.get(category_name=sub_category)

    new_budget = Budget.objects.create(
        budget_name=budget_name,
        budget_description=budget_description,
        budget_amount=float(budget_amount),
        category=budget_category,
        sub_category=budget_sub_category,
        owner=profile,
        account=account,
    )

    return new_budget


@login_required
def resolve_updateBudget(
    *_,
    id,
    budget_name: str,
    budget_description: str,
    budget_amount: str,
    category: str,
    sub_category: str,
):
    budget = Budget.objects.get(id=id)

    budget_category = (
        TransactionCategory.objects.get(category_name=category)
        if category
        else budget.category
    )

    budget_sub_category = (
        TransactionSubCategory.objects.get(category_name=sub_category)
        if sub_category
        else budget.sub_category
    )

    budget.budget_name = budget_name if budget_name else budget.budget_name
    budget.budget_description = (
        budget_description if budget_description else budget.budget_description
    )
    budget.budget_amount = (
        float(budget_amount) if budget_amount else budget.budget_amount
    )
    budget.category = budget_category
    budget.sub_category = budget_sub_category

    budget.save()

    return budget


@login_required
def resolve_budgetStatus(*_, id, status: bool):
    budget = Budget.objects.get(id=id)

    budget.budget_is_active = status

    budget.save()

    return True


@login_required
def resolve_deleteBudget(*_, id):
    try:
        budget = Budget.objects.get(id=id)

        budget.delete()

    except Exception as e:
        raise Exception(str(e))

    return True
