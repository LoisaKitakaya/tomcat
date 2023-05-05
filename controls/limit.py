from billing.models import Plan
from targets.models import Target
from budgets.models import Budget
from accounts.models import Account
from users.models import User, Profile


def check_create_account_limit(user_id):
    user = User.objects.get(id=user_id)

    profile = Profile.objects.get(user__id=user.pk)

    all_accounts = Account.objects.filter(owner=profile).all()

    plan = profile.Plan.name

    if plan == "Free":
        plan = Plan.objects.get(name="Free")

        account_limit = plan.no_of_accounts

        if len(all_accounts) != account_limit:
            return
        else:
            raise Exception(
                "You cannot create more accounts based on your current plan"
            )

    elif plan == "Standard":
        plan = Plan.objects.get(name="Standard")

        account_limit = plan.no_of_accounts

        if len(all_accounts) != account_limit:
            return
        else:
            raise Exception(
                "You cannot create more accounts based on your current plan"
            )

    elif plan == "Pro":
        plan = Plan.objects.get(name="Pro")

        account_limit = plan.no_of_accounts

        if len(all_accounts) != account_limit:
            return
        else:
            raise Exception(
                "You cannot create more accounts based on your current plan"
            )


def check_create_budget_limit(user_id):
    user = User.objects.get(id=user_id)

    profile = Profile.objects.get(user__id=user.pk)

    user_account = Account.objects.get(owner=profile)

    all_budgets = Budget.objects.filter(account=user_account).all()

    plan = profile.plan.name

    if plan == "Free":
        plan = Plan.objects.get(name="Free")

        budget_limit = plan.no_of_budgets

        if len(all_budgets) != budget_limit:
            return

        else:
            raise Exception("you cannot create more budgets based on you current plan")

    elif plan == "Standard":
        plan = Plan.objects.get(name="Standard")

        budget_limit = plan.no_of_budgets

        if len(all_budgets) != budget_limit:
            return

        else:
            raise Exception("you cannot create more budgets based on you current plan")

    elif plan == "Pro":
        plan = Plan.objects.get(name="Pro")

        budget_limit = plan.no_of_budgets

        if len(all_budgets) != budget_limit:
            return

        else:
            raise Exception("you cannot create more budgets based on you current plan")


def check_create_target_limit(user_id):
    user = User.objects.get(id=user_id)

    profile = Profile.objects.get(user__id=user.pk)

    user_account = Account.objects.get(owner=profile)

    all_targets = Target.objects.filter(account=user_account).all()

    plan = profile.plan.name

    if plan == "Free":
        plan = Plan.objects.get(name="Free")

        target_limit = plan.no_of_targets

        if len(all_targets) != target_limit:
            return

        else:
            raise Exception("You cannot create more targets based on your current plan")

    elif plan == "Standard":
        plan = Plan.objects.get(name="Standard")

        target_limit = plan.no_of_targets

        if len(all_targets) != target_limit:
            return

        else:
            raise Exception("You cannot create more targets based on your current plan")

    elif plan == "Pro":
        plan = Plan.objects.get(name="Pro")

        target_limit = plan.no_of_targets

        if len(all_targets) != target_limit:
            return

        else:
            raise Exception("You cannot create more targets based on your current plan")


def check_create_teams_limit(user_id):
    user = User.objects.get(id=user_id)

    profile = Profile.objects.get(user__id=user.pk)

    all_profiles = Profile.objects.filter(workspace_uid=profile.workspace_uid).all()

    plan = profile.plan.name

    if plan == "Free":
        plan = Plan.objects.get(name="Free")

        teams_limit = plan.no_of_teams

        if len(all_profiles) != teams_limit:
            return

        else:
            raise Exception("You cannot add more members giver your current plan")

    elif plan == "Standard":
        plan = Plan.objects.get(name="Standard")

        teams_limit = plan.no_of_teams

        if len(all_profiles) != teams_limit:
            return

        else:
            raise Exception("You cannot add more members giver your current plan")

    elif plan == "Pro":
        plan = Plan.objects.get(name="Pro")

        teams_limit = plan.no_of_teams

        if len(all_profiles) != teams_limit:
            return

        else:
            raise Exception("You cannot add more members giver your current plan")
