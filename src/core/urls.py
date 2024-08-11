from django.urls import path

from core.views.api import api_property_search
from core.views.order_cancel import cancel
from core.views.order_form import OrderForm
from core.views.order_status import order_status
from core.views.order_success import success
from core.webhooks.stripe import webhook_stripe
from core.views.api import get_certificate_bundles

urlpatterns = [
    path("", OrderForm.as_view(), name="order_form"),
    # Payment:
    path("order/success/", success, name="order_success"),
    path("order/cancel/", cancel, name="order_cancel"),
    path("order/<uuid:order_hash>/", order_status, name="order_status"),
    # Webhooks:
    path("webhook/stripe", webhook_stripe, name="webhook-stripe"),
    # API:
    path(
        "api/property/search/", api_property_search, name="api_property_search"
    ),
    path('api/get-certificate-bundles/', get_certificate_bundles, name='get_certificate_bundles'),
]
