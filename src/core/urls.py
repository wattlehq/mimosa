from django.urls import path

from core import views

from .webhooks.stripe import webhook_stripe

urlpatterns = [
    path("", views.home, name="home"),
    path("webhook/stripe", webhook_stripe, name="webhook-stripe"),
]
