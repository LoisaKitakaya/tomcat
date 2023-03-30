import pyotp
from ariadne_jwt.decorators import login_required
from users.models import User, Profile, OTPDevice, Package

# User model mutation resolvers


def resolve_createUser(
    *_, phone_number, email, first_name, last_name, password, password2
):

    if not User.objects.filter(email=email).exists():

        if len(password) > 8 and len(password2) > 8:

            if password == password2:

                User.objects.create(
                    email=email,
                    phone_number=phone_number,
                    first_name=first_name,
                    last_name=last_name,
                )

            else:

                raise Exception("Passwords provided did not match!")

            new_user = User.objects.get(email=email)

            new_user.set_password(password)

            new_user.save()

            name = f"OTP device for user: ID {new_user.id}"

            starter_package = Package.objects.get(name="Free")

            Profile.objects.create(user=new_user, package=starter_package)

            new_device = OTPDevice.objects.create(user=new_user, name=name)

            new_device.key = str(pyotp.random_base32())

            new_device.save()

        else:

            raise Exception("Password is too short. Must have minimum of 8 characters")

    else:

        raise Exception("Email already exists. Make sure your email is unique!")

    return new_user


@login_required
def resolve_verifyOTP(_, info, otp):

    pass

    request = info.context["request"]

    user = User.objects.get(id=request.user.id)

    device = OTPDevice.objects.get(user__id=user.id)

    totp = pyotp.TOTP(str(device.key))

    try:

        test = totp.verify(otp)

    except Exception as e:

        raise Exception(str(e))

    if test:

        return {
            "success": True,
            "message": f"Your account has been verified",
        }

    else:

        return {
            "success": False,
            "message": f"Entered invalid OTP code",
        }


@login_required
def resolve_updateUser(_, info, phone_number, email, first_name, last_name):

    request = info.context["request"]

    if not User.objects.filter(email=email).exists():

        if not User.objects.filter(phone_number=phone_number).exists():

            user = User.objects.get(id=request.user.id)

            user.email = email
            user.phone_number = phone_number
            user.first_name = first_name
            user.last_name = last_name

            user.save()

        else:

            raise Exception(
                "Phone number already exists. Make sure your Phone number is unique!"
            )

    else:

        raise Exception("Email already exists. Make sure your email is unique!")

    return user
