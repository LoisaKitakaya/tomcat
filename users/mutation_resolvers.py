from django_otp.oath import TOTP
from users.models import User, Profile
from ariadne_jwt.decorators import login_required
from django_otp.plugins.otp_totp.models import TOTPDevice

# User model mutation resolvers


def resolve_createUser(*_, username, email, first_name, last_name, password, password2):

    if not User.objects.filter(email=email).exists():

        if len(password) > 8 and len(password2) > 8:

            if password == password2:

                User.objects.create(
                    username=username,
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                )

            else:

                raise Exception("Passwords provided did not match!")

            new_user = User.objects.get(email=email)

            new_user.set_password(password)

            new_user.save()

            name = f"OTP device for user: ID {new_user.id}"

            Profile.objects.create(user=new_user)

            TOTPDevice.objects.create(user=new_user, name=name)

        else:

            raise Exception("Password is too short. Must have minimum of 8 characters")

    else:

        raise Exception("Email already exists. Make sure your email is unique!")

    return new_user


@login_required
def resolve_verifyOTP(_, info, otp):

    request = info.context["request"]

    user = User.objects.get(id=request.user.id)

    device = TOTPDevice.objects.get(user__id=user.id)

    secret = device.key.encode()

    totp = TOTP(key=secret)

    try:

        totp.verify(otp)

    except Exception as e:

        raise Exception(str(e))

    else:

        return {
            "success": True,
            "message": f"Your account has been verified",
        }


@login_required
def resolve_updateUser(_, info, username, email, first_name, last_name):

    request = info.context["request"]

    if not User.objects.filter(email=email).exists():

        if not User.objects.filter(username=username).exists():

            user = User.objects.get(id=request.user.id)

            user.username = username
            user.email = email
            user.first_name = first_name
            user.last_name = last_name

            user.save()

        else:

            raise Exception(
                "Username already exists. Make sure your username is unique!"
            )

    else:

        raise Exception("Email already exists. Make sure your email is unique!")

    return user
