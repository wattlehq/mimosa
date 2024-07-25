from django.urls import path

from core.views.home import home
from core.views.order import order
from core.views.find_parcel import FindParcel
from core.views.api import search_properties_view, validate_search_view
from core.webhooks.stripe import webhook_stripe

urlpatterns = [
    path("", home, name="home"),
    path("webhook/stripe", webhook_stripe, name="webhook-stripe"),
    path("certificate-order/", FindParcel.as_view(), name="find_parcel"),
    path("api/validate-search/",
         validate_search_view,
         name="api_validate_search"
         ),
    path("api/search-properties/",
         search_properties_view,
         name="api_search_properties"
         ),
    # @todo Obfuscate URL.
    path("order/<str:order_id>/", order, name="order"),
    path("order/<uuid:order_hash>/", order, name="order"),
]
