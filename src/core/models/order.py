from django.db import models
from django.utils import timezone

from .certificate import Certificate
from .property import Property


class Order(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
    )

    certificate = models.ManyToManyField(
        Certificate,
        through="OrderLine"
    )

    def __str__(self):
        return str(self.property) + " " + str(self.certificate)


class OrderLine(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
    )

    certificate = models.ForeignKey(
        Certificate,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return str(self.certificate)
