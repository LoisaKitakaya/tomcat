from plans.models import Plan
from users.models import Profile
from ariadne_jwt.decorators import login_required
from controls.decorators import check_plan_standard, check_plan_pro, check_is_employee


@login_required
@check_plan_standard
def resolve_testStandardDecorator(_, info):
    request = info.context["request"]

    profile = Profile.objects.get(user__id=request.user.id)

    plan = Plan.objects.get(name=profile.Plan.name)

    return plan


@login_required
@check_plan_pro
def resolve_testProDecorator(_, info):
    request = info.context["request"]

    profile = Profile.objects.get(user__id=request.user.id)

    plan = Plan.objects.get(name=profile.Plan.name)

    return plan


@login_required
@check_is_employee
def resolve_testIfIsEmployee(_, info):
    request = info.context["request"]

    profile = Profile.objects.get(user__id=request.user.id)

    assert profile.user.pk == request.user.id

    return True
