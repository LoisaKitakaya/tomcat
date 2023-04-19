import pyotp
from teams.models import Workspace
from billing.models import Package
from ariadne_jwt.decorators import login_required
from users.models import User, Profile, OTPDevice


@login_required
def resolve_updateWorkspace(_, info, name):
    request = info.context["request"]

    workspace = Workspace.objects.get(owner__id=request.user.id)

    workspace.name = name

    workspace.save()

    return workspace


@login_required
def resolve_createTeamMember(
    _, info, email, first_name, last_name, password
):
    if not User.objects.filter(email=email).exists():
        if len(password) > 8:
            request = info.context["request"]

            owner_profile = Profile.objects.get(user__id=request.user.id)

            workspace = Workspace.objects.get(owner__id=request.user.id)

            new_user = User.objects.create(
                email=email,
                username=email,
                first_name=first_name,
                last_name=last_name,
            )

            new_user.set_password(password)

            new_user.save()

            starter_package = Package.objects.get(id=owner_profile.package.pk)

            Profile.objects.create(
                user=new_user,
                is_employee=True,
                package=starter_package,
                workspace_uid=workspace.workspace_uid,
            )

            name = f"OTP device for user: ID {new_user.pk}"

            new_device = OTPDevice.objects.create(user=new_user, name=name)

            new_device.key = str(pyotp.random_base32())

            new_device.save()

        else:
            raise Exception("Password is too short. Must have minimum of 8 characters")

    else:
        raise Exception("Email already exists. Make sure the email is unique!")

    return new_user


@login_required
def resolve_deleteTeamMember(_, info, member_id):
    request = info.context["request"]

    workspace = Workspace.objects.get(owner__id=request.user.id)

    member = User.objects.get(id=member_id)

    member_profile = Profile.objects.get(user__id=member.pk)

    if member.pk == request.user.id:
        raise Exception("You cannot delete your own profile")

    try:
        if member_profile.workspace_uid == workspace.workspace_uid:
            member.delete()

        else:
            raise Exception("Invalid action")

    except Exception as e:
        raise Exception(str(e))

    else:
        return True
