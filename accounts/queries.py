from users.models import Profile
from accounts.models import Account
from ariadne_jwt.decorators import login_required


@login_required
def resolve_getAllAccounts(_, info):
    request = info.context["request"]

    profile = Profile.objects.get(user__id=request.user.id)

    accounts = Account.objects.filter(owner__id=profile.pk).all()

    return accounts


@login_required
def resolve_getAccount(*_, id):
    try:
        account = Account.objects.get(id=id)

    except Exception as e:
        raise Exception(str(e))

    return account
