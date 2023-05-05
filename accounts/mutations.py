from users.models import Profile
from accounts.models import Account
from teams.models import Workspace, TeamLogs
from ariadne_jwt.decorators import login_required


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
