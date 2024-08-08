import stripe
from django.conf import settings
from django.db import models
from django.utils import timezone

from core.models.property import Property

stripe.api_key = settings.STRIPE_SECRET_KEY


# Merges common fields between order and order_session.
class OrderBase(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    customer_name = models.CharField(max_length=254, null=True, blank=True)

    customer_company_name = models.CharField(
        max_length=200, null=True, blank=True
    )

    customer_phone = models.CharField(max_length=15, null=True, blank=True)

    customer_company_ref = models.CharField(
        max_length=200, null=True, blank=True
    )

    customer_address_street_line_1 = models.CharField(
        max_length=200, null=True, blank=True
    )

    customer_address_street_line_2 = models.CharField(
        max_length=200, null=True, blank=True
    )

    customer_address_suburb = models.CharField(
        max_length=50, null=True, blank=True
    )

    customer_address_state = models.CharField(
        max_length=3, null=True, blank=True
    )

    customer_address_post_code = models.CharField(
        max_length=4, null=True, blank=True
    )

    customer_address_country = models.CharField(
        max_length=3, null=True, blank=True
    )

    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
    )

    class Meta:
        abstract = True
