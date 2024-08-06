from django.urls import path

from core.views.api import api_property_search
from core.views.cancel import cancel
from core.views.find_parcel import FindParcel
from core.views.home import home
from core.views.order import order
from core.views.success import success
from core.webhooks.stripe import webhook_stripe

urlpatterns = [
    path("", home, name="home"),
    # @todo Rename
    path("certificate-order/", FindParcel.as_view(), name="find_parcel"),
    path("order/<uuid:order_hash>/", order, name="order"),
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
