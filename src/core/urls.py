from django.urls import path

from core.views.admin.order_send_email_status import order_send_email_status
from core.views.api import api_property_search
from core.views.order_cancel import cancel
from core.views.order_form import OrderForm
from core.views.order_status import order_status
from core.views.order_success import success
from core.webhooks.stripe import webhook_stripe

urlpatterns = [
    path("", OrderForm.as_view(), name="order_form"),
    # Payment:
    path("order/success/", success, name="order_success"),
    path("order/cancel/", cancel, name="order_cancel"),
    path("order/<uuid:order_hash>/", order_status, name="order_status"),
    # Webhooks:
    path("webhook/stripe", webhook_stripe, name="webhook-stripe"),
    # Admin:
    path(
        "admin/order/<int:order_id>/send-email-status/",
        order_send_email_status,
        name="admin_order_send_email_status",
    ),
    # API:
    path(
        "api/property/search/", api_property_search, name="api_property_search"
    ),
]
