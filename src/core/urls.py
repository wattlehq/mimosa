from django.urls import path

from core.views.home import home
from core.views.order import order
from core.webhooks.stripe import webhook_stripe

urlpatterns = [
    path("", home, name="home"),
    path("webhook/stripe", webhook_stripe, name="webhook-stripe"),
    # @todo Obfuscate URL.
    path("order/<str:order_id>/", order, name="order"),
]
