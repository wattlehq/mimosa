from django.db import models
from django.utils import timezone


class Property(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    assessment = models.CharField(50)
    lot = models.CharField(50)
    section = models.CharField(50)
    deposited_plan = models.CharField(50)

    address_street = models.CharField(50, null=True)
    address_suburb = models.CharField(50, null=True)
    address_state = models.CharField(50, null=True)
    address_post_code = models.CharField(50, null=True)

    def __str__(self):
        return self.address_street
