from plans.models import Plan
from users.models import Profile
from ariadne_jwt.decorators import login_required
from controls.decorators import check_plan_standard, check_plan_pro


@login_required
@check_plan_standard
def resolve_testStandardDecorator(_, info):
    request = info.context["request"]

    profile = Profile.objects.get(user__id=request.user.id)

    plan = Plan.objects.get(name=profile.plan.name)

    return plan


@login_required
@check_plan_pro
def resolve_testProDecorator(_, info):
    request = info.context["request"]

    profile = Profile.objects.get(user__id=request.user.id)

    plan = Plan.objects.get(name=profile.plan.name)

    return plan
