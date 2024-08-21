import uuid

from django.db import models

from core.models.abstract.order.base import OrderBase
from core.models.abstract.order.fulfillable import OrderFulfillable
from core.models.certificate import Certificate
from core.models.fee import Fee


class OrderSessionStatus(models.IntegerChoices):
    PENDING = 1, "Pending"
    COMPLETED = 2, "Completed"
    ERROR = 3, "Error"


class OrderSession(OrderBase):
    stripe_checkout_id = models.CharField(max_length=255)

    status = models.IntegerField(
        choices=OrderSessionStatus.choices, default=OrderSessionStatus.PENDING
    )

    status_error = models.CharField(max_length=255, null=True, blank=True)

    lines = models.ManyToManyField(Certificate, through="OrderSessionLine")

    def __str__(self):
        return str(self.property) + " - " + str(self.created_at)


class OrderSessionLine(models.Model):
    order_session = models.ForeignKey(
        OrderSession,
        on_delete=models.CASCADE,
    )

    certificate = models.ForeignKey(
        Certificate,
        on_delete=models.CASCADE,
    )

    fee = models.ForeignKey(
        Fee, on_delete=models.CASCADE, null=True, blank=True
    )

    cost_certificate = models.DecimalField(max_digits=10, decimal_places=2)
    cost_fee = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    tax_amount_certificate = models.DecimalField(
        max_digits=10, decimal_places=2, default=0
    )
    tax_amount_fee = models.DecimalField(
        max_digits=10, decimal_places=2, default=0
    )

    def __str__(self):
        return str(self.certificate) + " " + str(self.fee)


class Order(OrderBase, OrderFulfillable):
    order_hash = models.UUIDField(default=uuid.uuid4, unique=True)

    customer_email = models.EmailField(max_length=254)

    lines = models.ManyToManyField(Certificate, through="OrderLine")

    order_session = models.ForeignKey(
        OrderSession,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    stripe_payment_intent = models.CharField(
        max_length=254,
        null=True,
        blank=True,
    )

    def save(self, *args, **kwargs):
        super(Order, self).fulfilled_save(*args, **kwargs)

    def __str__(self):
        return str(self.property)


def certificate_file_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/certificates/order_<hash>/<filename>
    return "certificates/order_{0}/{1}".format(
        instance.order.order_hash, filename
    )


class OrderLine(OrderFulfillable):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
    )

    certificate = models.ForeignKey(
        Certificate,
        on_delete=models.CASCADE,
    )

    certificate_file = models.FileField(
        upload_to=certificate_file_directory_path, null=True, blank=True
    )

    fee = models.ForeignKey(
        Fee, on_delete=models.CASCADE, null=True, blank=True
    )

    cost_certificate = models.DecimalField(max_digits=10, decimal_places=2)
    cost_fee = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    tax_amount_certificate = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    tax_amount_fee = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )

    def save(self, *args, **kwargs):
        super(OrderLine, self).fulfilled_save(*args, **kwargs)

    def __str__(self):
        return str(self.certificate)
