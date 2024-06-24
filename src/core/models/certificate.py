from core.services.certificate.stripe import sync_to_stripe_new, \
    sync_to_stripe_existing
from django.db import models
from django.utils import timezone

from .fee import Fee


class Certificate(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    stripe_product_id = models.CharField(max_length=100, blank=True, null=True)
    stripe_price_id = models.CharField(max_length=100, blank=True, null=True)

    # @todo Make optional
    fees = models.ManyToManyField(
        Fee,
        related_name="fees"
    )

    def save(self, *args, **kwargs):
        # @todo Move sync logic to function inside model file.
        is_new = self.pk is None
        if is_new:
            sync_product_id, sync_price_id = sync_to_stripe_new(
                name_new=self.name,
                price_new=self.price,
            )
            self.stripe_product_id = sync_product_id
            self.stripe_price_id = sync_price_id
        else:
            original = Certificate.objects.get(pk=self.pk)
            sync_product_id, sync_price_id = sync_to_stripe_existing(
                product_id=self.stripe_product_id,
                price_id=self.stripe_price_id,
                name_new=self.name,
                name_old=original.name,
                price_new=self.price,
                price_old=original.price
            )
            self.stripe_product_id = sync_product_id
            self.stripe_price_id = sync_price_id

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
