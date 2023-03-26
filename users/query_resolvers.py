from twilio.rest import Client
from django.conf import settings
from django_otp.oath import TOTP
from users.models import User, Profile
from ariadne_jwt.decorators import login_required
from django_otp.plugins.otp_totp.models import TOTPDevice

# User model query resolvers


@login_required
def resolve_getAllUsers(*_):

    try:

        all_users = User.objects.all()

    except Exception as e:

        raise Exception(str(e))

    return all_users


@login_required
def resolve_getUser(_, info):

    request = info.context["request"]

    try:

        user = User.objects.get(id=request.user.id)

    except Exception as e:

        raise Exception(str(e))

    return user


@login_required
def resolve_getUserByUsername(*_, username):

    try:

        user = User.objects.get(username=username)

    except Exception as e:

        raise Exception(str(e))

    return user


@login_required
def resolve_generateOTP(_, info):

    request = info.context["request"]

    user = User.objects.get(id=request.user.id)

    device = TOTPDevice.objects.get(user__id=user.id)

    secret = device.key.encode()

    totp = TOTP(key=secret)

    otp = totp.token()

    account = settings.TWILIO_ACCOUNT
    token = settings.TWILIO_TOKEN
    number = settings.TWILIO_NUMBER

    client = Client(account, token)

    message = client.messages.create(
        body=f"Your One-Time-Password is:\n{otp}", from_=number, to=user.phone_number
    )
    print(message.sid)

    return True


# Profile model query resolvers


@login_required
def resolve_getAllProfiles(*_):

    try:

        profiles = Profile.objects.all()

    except Exception as e:

        raise Exception(str(e))

    return profiles


@login_required
def resolve_getProfile(_, info):

    request = info.context["request"]

    try:

        profile = Profile.objects.get(user__id=request.user.id)

    except Exception as e:

        raise Exception(str(e))

    return profile
