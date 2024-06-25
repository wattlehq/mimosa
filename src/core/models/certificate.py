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
        is_new = self.pk is None

        if is_new:
            certificate_old = None
        else:
            certificate_old = Certificate.objects.get(pk=self.pk)

        # Must save first so a PK is available for Stripe.
        super(Certificate, self).save(*args, **kwargs)

        sync_product_id, sync_price_id = sync_to_stripe(certificate_old, self)
        self.stripe_product_id = sync_product_id
        self.stripe_price_id = sync_price_id

        # Must save Stripe IDs to DB.
        super(Certificate, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


def sync_to_stripe(certificate_old: Certificate, certificate_new: Certificate):
    if certificate_old is None:
        return sync_to_stripe_new(
            name_new=certificate_new.name,
            price_new=certificate_new.price,
            pk=str(certificate_new.pk),
        )
    else:
        return sync_to_stripe_existing(
            product_id=certificate_old.stripe_product_id,
            price_id=certificate_old.stripe_price_id,
            name_new=certificate_new.name,
            name_old=certificate_old.name,
            price_new=certificate_new.price,
            price_old=certificate_old.price
        )
