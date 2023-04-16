from django.db.models import Q
from django.conf import settings
from django.core.mail import send_mail
from users.models import Profile, Package
from ariadne_jwt.decorators import login_required
from billing.models import PlanBilling
