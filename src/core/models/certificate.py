from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from core.models.abstract.stripe_product import StripeProduct
from core.models.fee import Fee


class Certificate(StripeProduct):
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    description = models.CharField(max_length=255, null=True, blank=True)
    account_code = models.CharField(max_length=10)

    fees = models.ManyToManyField(Fee, related_name="fees", blank=True)

    child_certificates = models.ManyToManyField(
        "self",
        symmetrical=False,
        related_name="parent_certificates",
        blank=True,
    )

    def clean(self):
        super().clean()
        if self.pk and self in self.child_certificates.all():
            raise ValidationError("A certificate cannot be its own child.")

    def save(self, *args, **kwargs):
        super(Certificate, self).stripe_save_sync(*args, **kwargs)

    def __str__(self):
        return self.name
