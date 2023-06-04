from users.models import Profile
from accounts.models import Account
from ariadne_jwt.decorators import login_required


@login_required
def resolve_createAccount(
    _,
    info,
    account_name: str,
    account_type: str,
    account_balance: str,
    currency_code: str,
):
    request = info.context["request"]

    profile = Profile.objects.get(user__id=request.user.id)

    new_account = Account.objects.create(
        account_name=account_name,
        account_type=account_type,
        account_balance=float(account_balance),
        currency_code=currency_code,
        owner=profile,
    )

    return new_account


@login_required
def resolve_updateAccount(
    *_,
    id,
    account_name: str,
    account_type: str,
    account_balance: str,
    currency_code: str,
):
    account = Account.objects.get(id=id)

    account.account_name = account_name if account_name else account.account_name
    account.account_type = account_type if account_type else account.account_type
    account.account_balance = (
        float(account_balance) if account_balance else account.account_balance
    )
    account.currency_code = currency_code if currency_code else account.currency_code

    account.save()

    return account


@login_required
def resolve_deleteAccount(*_, id):
    try:
        account = Account.objects.get(id=id)

        account.delete()

    except Exception as e:
        raise Exception(str(e))

    return True
