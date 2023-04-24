from teams.models import Workspace
from app.models import Account, Budget, Target
from users.models import User, Profile, Package

def check_create_account_limit(user_id):
    user = User.objects.get(id=user_id)

    profile = Profile.objects.get(user__id=user.pk)

    plan = profile.package.name

    if plan == "Free":
        package = Package.objects.get(name="Free")

        all_accounts = Account.objects.filter(owner=user).all()

    elif plan == "Standard":
        package = Package.objects.get(name="Standard")

        all_accounts = Account.objects.filter(owner=user).all()

    elif plan == "Pro":
        package = Package.objects.get(name="Pro")

        all_accounts = Account.objects.filter(owner=user).all()

def check_create_budget_limit(user_id):
    user = User.objects.get(id=user_id)

    profile = Profile.objects.get(user__id=user.pk)

    plan = profile.package.name

    if plan == "Free":
        package = Package.objects.get(name="Free")

        user_account = Account.objects.get(owner=user)

        all_budgets = Budget.objects.filter(account=user_account).all()

    elif plan == "Standard":
        package = Package.objects.get(name="Standard")

        user_account = Account.objects.get(owner=user)

        all_budgets = Budget.objects.filter(account=user_account).all()

    elif plan == "Pro":
        package = Package.objects.get(name="Pro")

        user_account = Account.objects.get(owner=user)

        all_budgets = Budget.objects.filter(account=user_account).all()

def check_create_target_limit(user_id):
    user = User.objects.get(id=user_id)

    profile = Profile.objects.get(user__id=user.pk)

    plan = profile.package.name

    if plan == "Free":
        package = Package.objects.get(name="Free")

        user_account = Account.objects.get(owner=user)

        all_targets = Target.objects.filter(account=user_account).all()

    elif plan == "Standard":
        package = Package.objects.get(name="Standard")

        user_account = Account.objects.get(owner=user)

        all_targets = Target.objects.filter(account=user_account).all()

    elif plan == "Pro":
        package = Package.objects.get(name="Pro")

        user_account = Account.objects.get(owner=user)

        all_targets = Target.objects.filter(account=user_account).all()

def check_create_teams_limit(user_id):
    user = User.objects.get(id=user_id)

    profile = Profile.objects.get(user__id=user.pk)

    workspace = Workspace.objects.get(workspace_uid=profile.workspace_uid)

    plan = profile.package.name

    if plan == "Free":
        package = Package.objects.get(name="Free")

    elif plan == "Standard":
        package = Package.objects.get(name="Standard")

    elif plan == "Pro":
        package = Package.objects.get(name="Pro")