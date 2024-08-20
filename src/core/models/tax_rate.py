import stripe
from django.conf import settings
from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone

from core.services.tax_rate.create_stripe_tax_rate import (
    create_stripe_tax_rate,
)
from core.services.tax_rate.update_stripe_tax_rate import (
    update_stripe_tax_rate,
)

stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_base = settings.STRIPE_API_BASE


class TaxRate(models.Model):
    name = models.CharField(max_length=100, unique=True)
    percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(1), MaxValueValidator(100)],
    )
    stripe_tax_rate_id = models.CharField(
        max_length=100, blank=True, null=True
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Tax Rate"
        verbose_name_plural = "Tax Rates"

    def __str__(self):
        return f"{self.name} ({self.percentage}%)"

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)

        if is_new:
            success = create_stripe_tax_rate(self)
        else:
            success = update_stripe_tax_rate(self)

        if not success:
            print(f"Failed to sync tax rate {self.name} with Stripe")
