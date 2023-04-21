import io
import pyotp
import base64
from django.conf import settings
from qrcode import make as make_qr
from django.core.mail import send_mail
from ariadne_jwt.decorators import login_required
from users.models import User, Profile, OTPDevice

# User model query resolvers


@login_required
def resolve_getUser(_, info):
    request = info.context["request"]

    try:
        user = User.objects.get(id=request.user.id)

    except Exception as e:
        raise Exception(str(e))

    return user


@login_required
def resolve_generateOTP(_, info):
    request = info.context["request"]

    user = User.objects.get(id=request.user.id)

    device = OTPDevice.objects.get(user__id=user.pk)

    totp = pyotp.TOTP(str(device.key))

    otp = totp.now()

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

    device = OTPDevice.objects.get(user__id=user.pk)

    totp_uri = pyotp.totp.TOTP(str(device.key)).provisioning_uri(
        name=user.email, issuer_name="Finance Fluent 2FA"
    )
    qr = make_qr(totp_uri)

    img = qr.get_image()
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    image_base64 = base64.b64encode(buf.getvalue()).decode("ascii")

    return image_base64


# Profile model query resolvers


@login_required
def resolve_getProfile(_, info):
    request = info.context["request"]

    try:
        profile = Profile.objects.get(user__id=request.user.id)

    except Exception as e:
        raise Exception(str(e))

    return profile
