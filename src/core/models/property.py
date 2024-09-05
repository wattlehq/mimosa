from django.db import models
from django.utils import timezone


class Property(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    assessment = models.CharField(max_length=50, db_index=True)
    lot = models.CharField(max_length=50, db_index=True)
    section = models.CharField(max_length=50, db_index=True)
    deposited_plan = models.CharField(max_length=50, db_index=True)

    address_street = models.CharField(max_length=50, null=True)
    address_suburb = models.CharField(max_length=50, null=True)
    address_state = models.CharField(max_length=50, null=True)
    address_post_code = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.address_street

    class Meta:
        verbose_name_plural = "properties"
