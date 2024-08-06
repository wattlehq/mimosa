from django.urls import path

from core.views.api import api_property_search
from core.views.cancel import cancel
from core.views.find_parcel import FindParcel
from core.views.home import home
from core.views.order import order
from core.views.order_create import OrderCreate
from core.views.success import success
from core.webhooks.stripe import webhook_stripe

urlpatterns = [
    path("", home, name="home"),
    path("success/", success, name="success"),
    path("webhook/stripe", webhook_stripe, name="webhook-stripe"),
    # @todo Merge certificate-order and order-create
    path("certificate-order/", FindParcel.as_view(), name="find_parcel"),
    path("order-create/", OrderCreate.as_view(), name="order_create"),
    path(
        "api/property/search/", api_property_search, name="api_property_search"
    ),
    path("order/<uuid:order_hash>/", order, name="order"),
    path("cancel/", cancel, name="cancel"),
]
