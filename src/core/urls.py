from django.urls import path
from .views.find_parcel import FindParcel
from .views.home import home
from core.webhooks.stripe import webhook_stripe

urlpatterns = [
    path("", home, name="home"),
    path("webhook/stripe", webhook_stripe, name="webhook-stripe"),
    path('certificate-order/', FindParcel.as_view(), name='find_parcel')
]