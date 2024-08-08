from django.urls import path

from core.views.api import api_property_search
from core.views.cancel import cancel
from core.views.order_form import OrderForm
from core.views.order_status import order_status
from core.views.success import success
from core.webhooks.stripe import webhook_stripe

urlpatterns = [
    path("", OrderForm.as_view(), name="order_form"),
    path("order/<uuid:order_hash>/", order_status, name="order"),
    # Payment:
    path("success/", success, name="success"),
    path("cancel/", cancel, name="cancel"),
    # Webhooks:
    path("webhook/stripe", webhook_stripe, name="webhook-stripe"),
    # API:
    path(
        "api/property/search/", api_property_search, name="api_property_search"
    ),
]
