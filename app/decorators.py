import functools
from users.models import Profile


def check_plan_standard(info):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            request = info.context["request"]

            profile = Profile.objects.get(user__id=request.user.id)

            allowed = ["Standard, Pro"]

            plan = profile.package.name

            if plan in allowed:
                return func(*args, **kwargs)

            else:
                raise Exception(
                    "You cannot access this resource given your current plan"
                )

        return wrapper

    return decorator


def check_plan_pro(info):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            request = info.context["request"]

            profile = Profile.objects.get(user__id=request.user.id)

            allowed = ["Pro"]

            plan = profile.package.name

            if plan in allowed:
                return func(*args, **kwargs)

            else:
                raise Exception(
                    "You cannot access this resource given your current plan"
                )

        return wrapper

    return decorator
