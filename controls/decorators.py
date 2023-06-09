import functools
from users.models import Profile


def check_plan_standard(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        info = args[1]

        request = info.context["request"]

        profile = Profile.objects.get(user__id=request.user.id)

        allowed = ["Standard", "Pro"]

        plan = profile.plan.name

        if plan in allowed:
            return func(*args, **kwargs)

        else:
            raise Exception("You cannot access this resource given your current plan")

    return wrapper


def check_plan_pro(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        info = args[1]

        request = info.context["request"]

        profile = Profile.objects.get(user__id=request.user.id)

        allowed = ["Pro"]

        plan = profile.plan.name

        if plan in allowed:
            return func(*args, **kwargs)

        else:
            raise Exception("You cannot access this resource given your current plan")

    return wrapper
