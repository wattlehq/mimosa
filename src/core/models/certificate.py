from django.db import models
from django.utils import timezone

from .fee import Fee


class Certificate(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255)

    fees = models.ManyToManyField(
        Fee,
        related_name="fees"
    )

    def __str__(self):
        return self.name
