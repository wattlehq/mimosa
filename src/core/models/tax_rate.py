import stripe
from django.conf import settings
from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone

stripe.api_key = settings.STRIPE_SECRET_KEY


class TaxRate(models.Model):
    name = models.CharField(max_length=100, unique=True)
    percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
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
        self.stripe_save_sync()
        super().save(*args, **kwargs)

    def stripe_save_sync(self):
        if not self.stripe_tax_rate_id:
            self._create_stripe_tax_rate()
        else:
            self._update_stripe_tax_rate()

    def _create_stripe_tax_rate(self):
        stripe_tax_rate = stripe.TaxRate.create(
            display_name=self.name,
            description=f"{self.name} Tax Rate",
            percentage=float(self.percentage),
            inclusive=False,  # Assuming tax is not included in the price
            active=self.is_active,
            metadata={"tax_rate_id": str(self.id)},
        )
        self.stripe_tax_rate_id = stripe_tax_rate.id

    # Stripe only lets you update these TaxRate fields :/
    def _update_stripe_tax_rate(self):
        stripe.TaxRate.modify(
            self.stripe_tax_rate_id,
            active=self.is_active,
            metadata={"tax_rate_id": str(self.id)},
        )

    @classmethod
    def get_active_tax_rate(cls):
        return cls.objects.filter(is_active=True).first()
