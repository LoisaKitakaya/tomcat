from django.urls import path
from billing import views

urlpatterns = [
    path(
        "notifications/",
        views.notifications,  # type: ignore
        name="transaction-notifications",
    ),
    path(
        "pesapal_ipn_callback",
        views.pesapal_ipn_callback,  # type: ignore
        name="pesapal-ipn-callbacks",
    ),
]
