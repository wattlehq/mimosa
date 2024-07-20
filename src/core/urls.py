from django.urls import path

from core.webhooks.stripe import webhook_stripe

from .views.find_parcel import FindParcel
from .views.home import home

urlpatterns = [
    path("", home, name="home"),
    path("webhook/stripe", webhook_stripe, name="webhook-stripe"),
    path("certificate-order/", FindParcel.as_view(), name="find_parcel"),
]
