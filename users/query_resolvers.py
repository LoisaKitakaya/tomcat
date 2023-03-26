import base64
import io
from PIL import Image
from twilio.rest import Client
from django.conf import settings
from django_otp.oath import TOTP
from qrcode import make as make_qr
from users.models import User, Profile
from django.core.mail import send_mail
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

    if user.phone_number:

        account = settings.TWILIO_ACCOUNT
        token = settings.TWILIO_TOKEN
        number = settings.TWILIO_NUMBER

        client = Client(account, token)

        client.messages.create(
            body=f"Your One-Time-Password is:\n{otp}",
            from_=number,
            to=user.phone_number,
        )

        return {
            "success": True,
            "message": f"A One-Time-Password has been sent to the number:\n{user.phone_number}",
        }

    else:

        subject = "Account verification"
        body = f"Your One-Time-Password is:\n{otp}"
        me = settings.DEFAULT_FROM_EMAIL
        recipient = user.email

        send_mail(
            subject,
            body,
            me,
            [recipient],
            fail_silently=False,
        )

        return {
            "success": True,
            "message": f"A One-Time-Password has been sent to the email:\n{user.email}",
        }


@login_required
def resolve_generateQRCode(_, info):

    request = info.context["request"]

    user = User.objects.get(id=request.user.id)

    device = TOTPDevice.objects.get(user__id=user.id)

    totp_uri = device.config_url
    qr = make_qr(totp_uri)

    img = qr.get_image()
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    image_base64 = base64.b64encode(buf.getvalue()).decode("ascii")

    return image_base64


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
