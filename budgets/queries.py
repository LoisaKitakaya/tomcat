from users.models import Profile
from budgets.models import Budget
from teams.models import Workspace
from ariadne_jwt.decorators import login_required


@login_required
def resolve_getAllBudgets(_, info):
    request = info.context["request"]

    profile = Profile.objects.get(user__id=request.user.id)

    workspace = Workspace.objects.get(workspace_uid=profile.workspace_uid)

    budgets = Budget.objects.filter(workspace__id=workspace.pk).all()

    return budgets


@login_required
def resolve_getBudget(*_, id):
    try:
        budget = Budget.objects.get(id=id)

    except Exception as e:
        raise Exception(str(e))

    return budget
