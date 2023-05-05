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
    target_name,
    target_description,
    target_amount,
    category,
    sub_category,
):
    request = info.context["request"]

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
