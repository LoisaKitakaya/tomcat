import io
import pyotp
import base64
from plans.models import Plan
from django.conf import settings
from qrcode import make as make_qr
from django.core.mail import send_mail
from ariadne_jwt.decorators import login_required
from users.models import User, Profile, OTPDevice


def resolve_validateOrCreateUser(
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
def resolve_getUser(_, info):
    request = info.context["request"]

    try:
        user = User.objects.get(id=request.user.id)

    except Exception as e:
        raise Exception(str(e))

    return user


@login_required
def resolve_generateOTP(_, info, environment: str = ""):
    request = info.context["request"]

    user = User.objects.get(id=request.user.id)

    device = OTPDevice.objects.get(user__id=user.pk)

    totp = pyotp.TOTP(str(device.key))

    otp = totp.now()

    payload = []

    payload.append(otp)

    if environment:
        payload.append(environment)

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

    return payload


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
