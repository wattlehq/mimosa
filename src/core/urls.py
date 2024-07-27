from django.urls import path

from core.webhooks.stripe import webhook_stripe
from .views.home import home
from .views import product_selection
from core.views import product_selection, create_checkout_session, payment_success, payment_cancel

urlpatterns = [
    path("", home, name="home"),
    path("webhook/stripe", webhook_stripe, name="webhook-stripe"),
    path('product-selection/', product_selection, name='product_selection'),
    path('create-checkout-session/', create_checkout_session, name='create_checkout_session'),
    path('payment-success/', payment_success, name='payment_success'),
    path('payment-cancel/', payment_cancel, name='payment_cancel')
]
