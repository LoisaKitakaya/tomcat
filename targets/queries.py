from users.models import Profile
from targets.models import Target
from teams.models import Workspace
from ariadne_jwt.decorators import login_required


@login_required
def resolve_getAllTargets(_, info):
    request = info.context["request"]

    profile = Profile.objects.get(user__id=request.user.id)

    targets = Target.objects.filter(owner__id=profile.pk).all()

    return targets


@login_required
def resolve_getTarget(*_, id):
    try:
        target = Target.objects.get(id=id)

    except Exception as e:
        raise Exception(str(e))

    return target
