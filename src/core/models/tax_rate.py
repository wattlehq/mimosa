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
