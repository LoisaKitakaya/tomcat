from users.models import Profile
from teams.models import Workspace, TeamLogs
from ariadne_jwt.decorators import login_required
from app.decorators import check_plan_standard


@login_required
# @check_plan_standard
def resolve_getWorkspace(_, info):
    request = info.context["request"]

    workspace = Workspace.objects.get(owner__id=request.user.id)

    return workspace


@login_required
# @check_plan_standard
def resolve_getTeamLogs(*_, workspace_id):
    workspace = Workspace.objects.get(id=workspace_id)

    logs = TeamLogs.objects.filter(workspace__id=workspace.pk).all()

    return logs


@login_required
# @check_plan_standard
def resolve_getTeamMembers(_, info):
    request = info.context["request"]

    workspace = Workspace.objects.get(owner__id=request.user.id)

    members = Profile.objects.filter(workspace_uid=workspace.workspace_uid).all()

    return members
