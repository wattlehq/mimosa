import stripe
from django.conf import settings
from django.db import models
from django.utils import timezone

stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_base = settings.STRIPE_API_BASE


class OrderFulfillable(models.Model):
    fulfilled_at = models.DateTimeField(null=True, blank=True, default=None)
    is_fulfilled = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def fulfilled_save(self, *args, **kwargs):
        """updated `fulfilled_at` when `fulfilled` is set"""
        if self.pk:
            manager = self.__class__._default_manager
            record_old = manager.get(pk=self.pk)
            if not record_old.is_fulfilled and self.is_fulfilled:
                self.fulfilled_at = timezone.now()
        super(OrderFulfillable, self).save(*args, **kwargs)
