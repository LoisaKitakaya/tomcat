from users.models import Profile
from targets.models import Target
from accounts.models import Account
from teams.models import Workspace, TeamLogs
from ariadne_jwt.decorators import login_required
from transactions.models import TransactionCategory, TransactionSubCategory


@login_required
def resolve_createTarget(
    _,
    info,
    account_id,
    target_name: str,
    target_description: str,
    target_amount: str,
    category: str,
    sub_category: str,
):
    request = info.context["request"]

    profile = Profile.objects.get(user__id=request.user.id)

    account = Account.objects.get(id=account_id)

    target_category = TransactionCategory.objects.get(category_name=category)
    target_sub_category = TransactionSubCategory.objects.get(category_name=sub_category)

    new_target = Target.objects.create(
        target_name=target_name,
        target_description=target_description,
        target_amount=float(target_amount),
        category=target_category,
        sub_category=target_sub_category,
        owner=profile,
        account=account,
    )

    return new_target


@login_required
def resolve_updateTarget(
    *_,
    id,
    target_name: str,
    target_description: str,
    target_amount: str,
    category: str,
    sub_category: str,
):
    target = Target.objects.get(id=id)

    target_category = (
        TransactionCategory.objects.get(category_name=category)
        if category
        else target.category
    )

    target_sub_category = (
        TransactionSubCategory.objects.get(category_name=sub_category)
        if sub_category
        else target.sub_category
    )

    target.target_name = target_name if target_name else target.target_name
    target.target_description = (
        target_description if target_description else target.target_description
    )
    target.target_amount = (
        float(target_amount) if target_amount else target.target_amount
    )
    target.category = target_category
    target.sub_category = target_sub_category

    target.save()

    return target


@login_required
def resolve_targetStatus(*_, id, status: bool):
    target = Target.objects.get(id=id)

    target.target_is_active = status

    target.save()

    return True


@login_required
def resolve_deleteTarget(*_, id):
    try:
        target = Target.objects.get(id=id)

        target.delete()

    except Exception as e:
        raise Exception(str(e))

    return True
