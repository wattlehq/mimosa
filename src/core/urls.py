from django.urls import path

from core.webhooks.stripe import webhook_stripe
from .views.home import home
from .views import product_selection

urlpatterns = [
    path("", home, name="home"),
    path("webhook/stripe", webhook_stripe, name="webhook-stripe"),
    path('product-selection/', product_selection, name='product_selection')
]
