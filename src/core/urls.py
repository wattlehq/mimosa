from django.urls import path

from core.views.home import home
from core.views.order import order
from core.webhooks.stripe import webhook_stripe

urlpatterns = [
    path("", home, name="home"),
    path("webhook/stripe", webhook_stripe, name="webhook-stripe"),
    path("order/<uuid:order_hash>/", order, name="order"),
]
