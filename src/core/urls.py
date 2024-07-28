from django.urls import path

from core.views.api import api_property_search
from core.views.find_parcel import FindParcel
from core.views.home import home
from core.views.order import order
from core.views.success import success
from core.webhooks.stripe import webhook_stripe

urlpatterns = [
    path("", home, name="home"),
    path("success/", success, name="success"),
    path("webhook/stripe", webhook_stripe, name="webhook-stripe"),
    path("certificate-order/", FindParcel.as_view(), name="find_parcel"),
    path("api/property/search/",
         api_property_search,
         name="api_property_search"
         ),
    path("order/<uuid:order_hash>/", order, name="order"),
]
