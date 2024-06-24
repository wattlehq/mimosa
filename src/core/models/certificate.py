import stripe
from django.conf import settings
from django.db import models
from django.utils import timezone

from .fee import Fee

stripe.api_key = settings.STRIPE_API_SECRET_KEY


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
        original = Certificate.objects.get(pk=self.pk)
        price_cents = int(self.price * 100)

        super().save(*args, **kwargs)

        # @todo Get Stripe webhook working.
        if is_new:
            # @todo save PK to product.
            product = stripe.Product.create(name=self.name)

            price_cents = stripe.Price.create(
                product=product.stripe_id,
                unit_amount=price_cents,  # Stripe expects the amount in cents
                currency=settings.STRIPE_CURRENCY
            )

            self.stripe_product_id = product.id
            self.stripe_price_id = price_cents.id
            super().save(*args, **kwargs)
        else:
            if self.stripe_product_id and self.stripe_price_id:
                if original.name != self.name:
                    stripe.Product.modify(self.stripe_product_id,
                                          name=self.name)
                if original.price != self.price:
                    stripe.Price.modify(self.stripe_price_id, active=False)

                    new_price = stripe.Price.create(
                        product=self.stripe_product_id,
                        unit_amount=price_cents,
                        currency=settings.STRIPE_CURRENCY
                    )
                    self.stripe_price_id = new_price.id

        super(Certificate, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
