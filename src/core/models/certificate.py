from django.db import models
from django.utils import timezone


class Certificate(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=255)


def __str__(self):
    return self.name
