from django.urls import path

from core.webhooks.stripe import webhook_stripe

from core.views.find_parcel import FindParcel
from core.views.api import search_properties_view
from core.views.home import home

urlpatterns = [
    path("", home, name="home"),
    path("webhook/stripe", webhook_stripe, name="webhook-stripe"),
    path("certificate-order/", FindParcel.as_view(), name="find_parcel"),
    path("api/search-properties/",
         search_properties_view,
         name="api_search_properties"
         ),
]
