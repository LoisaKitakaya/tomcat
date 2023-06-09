import pyotp
from plans.models import Plan
from ariadne_jwt.decorators import login_required
from users.models import User, Profile, OTPDevice


def resolve_createUser(
    *_, email: str, first_name: str, last_name: str, password: str, password2: str
):
    if not User.objects.filter(email=email).exists():
        if len(password) > 8 and len(password2) > 8:
            if password == password2:
                User.objects.create(
                    email=email,
                    username=email,
                    first_name=first_name,
                    last_name=last_name,
                )

            else:
                raise Exception("Passwords provided did not match!")

            new_user = User.objects.get(email=email)

            new_user.set_password(password)

            new_user.save()

            starter_plan = Plan.objects.get(name="Free")

            Profile.objects.create(
                user=new_user,
                plan=starter_plan,
            )

            name = f"2FA Device For: {new_user.username}"

            OTPDevice.objects.create(
                user=new_user, name=name, key=str(pyotp.random_base32())
            )

        else:
            raise Exception("Password is too short. Must have minimum of 8 characters")

        return new_user

    else:
        existing_user = User.objects.filter(email=email).first()

    return existing_user


@login_required
def resolve_verifyOTP(_, info, otp: str):
    request = info.context["request"]

    user = User.objects.get(id=request.user.id)

    device = OTPDevice.objects.get(user__id=user.pk)

    totp = pyotp.TOTP(str(device.key))

    test = totp.verify(otp)

    if test:
        return "Your account has been verified"

    else:
        raise Exception("Entered invalid OTP code")


@login_required
def resolve_updateUser(_, info, email: str, first_name: str, last_name: str):
    request = info.context["request"]

    if not User.objects.filter(email=email).exists():
        user = User.objects.get(id=request.user.id)

        user.email = email if email else user.email
        user.username = email if email else user.username
        user.first_name = first_name if first_name else user.first_name
        user.last_name = last_name if last_name else user.last_name

        user.save()

    else:
        raise Exception("Email already exists. Make sure your email is unique!")

    return user
