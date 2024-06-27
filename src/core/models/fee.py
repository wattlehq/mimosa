from core.models.abstract.stripe_product import StripeProduct
from django.db import models
from django.utils import timezone


class Fee(StripeProduct):
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        super(Fee, self).stripe_save_sync(*args, **kwargs)

    def __str__(self):
        return self.name
