from uuid import uuid4
from users.models import Profile
from ariadne_jwt.decorators import login_required
from app.models import Account, Category, Budget, Transaction, Report

# account model mutation resolvers


@login_required
def resolve_createAccount(
    _, info, account_name, account_type, account_balance, currency_code
):

    request = info.context["request"]

    owner = Profile.objects.get(user__public_id=request.user.public_id)

    new_account = Account.objects.create(
        account_name=account_name,
        account_type=account_type,
        account_balance=account_balance,
        currency_code=currency_code,
        owner=owner,
    )

    new_account.public_id = str(uuid4().hex)

    new_account.save()

    return new_account


@login_required
def resolve_updateAccount(
    *_, public_id, account_name, account_type, account_balance, currency_code
):

    account = Account.objects.get(public_id=public_id)

    account.account_name = account_name
    account.account_type = account_type
    account.account_balance = account_balance
    account.currency_code = currency_code

    account.save()

    return account
