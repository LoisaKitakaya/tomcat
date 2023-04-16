from django.urls import path
from billing import views

urlpatterns = [
    path(
        "/transactions/",
        views.notifications,  # type: ignore
        name="transaction-notifications",
    ),
]
