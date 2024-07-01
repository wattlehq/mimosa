from core.models.abstract.stripe_product import StripeProduct
from django.db import models
from django.utils import timezone

from .fee import Fee


class Certificate(StripeProduct):
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    fees = models.ManyToManyField(
        Fee,
        related_name="fees",
        blank=True
    )

    def save(self, *args, **kwargs):
        super(Certificate, self).stripe_save_sync(*args, **kwargs)

    def __str__(self):
        return self.name
