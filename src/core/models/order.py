from django.db import models
from django.utils import timezone

from core.models.certificate import Certificate
from core.models.fee import Fee
from core.models.property import Property


# @todo Implement status
# @todo Implement customer details?
# @todo Implement better __str__
class OrderSession(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    stripe_checkout_id = models.CharField(max_length=255)

    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
    )

    # @todo Is "through" correct?
    lines = models.ManyToManyField(
        Certificate,
        through="OrderSessionLine"
    )

    def __str__(self):
        return str(self.property) + " " + str(self.lines)


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
        Fee,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    def __str__(self):
        return str(self.certificate) + " " + str(self.fee)


# @todo Implement better __str__
# @todo Implement Stripe Order ID.
class Order(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_fulfilled = models.BooleanField(default=False)

    customer_email = models.EmailField(max_length=254)
    customer_phone = models.CharField(max_length=15, null=True)
    customer_company_name = models.CharField(max_length=200, null=True)
    customer_company_ref = models.CharField(max_length=200, null=True)
    customer_address_street_line_1 = models.CharField(
        max_length=200, null=True
    )
    customer_address_street_line_2 = models.CharField(
        max_length=200, null=True
    )
    customer_address_suburb = models.CharField(max_length=50, null=True)
    customer_address_state = models.CharField(max_length=3, null=True)
    customer_address_post_code = models.CharField(max_length=4, null=True)
    customer_address_country = models.CharField(max_length=3, null=True)

    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
    )

    # @todo Is "through" correct?
    lines = models.ManyToManyField(Certificate, through="OrderLine")

    order_session = models.ForeignKey(
        OrderSession,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    def __str__(self):
        return str(self.property) + " " + str(self.lines)


def certificate_file_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/certificates/order_<id>/<filename>
    return "certificates/order_{0}/{1}".format(
        instance.lines.id, filename
    )


class OrderLine(models.Model):
    is_fulfilled = models.BooleanField(default=False)

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
    )

    certificate = models.ForeignKey(
        Certificate,
        on_delete=models.CASCADE,
    )

    certificate_file = models.FileField(
        upload_to=certificate_file_directory_path,
        null=True
    )

    fee = models.ForeignKey(
        Fee,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    def __str__(self):
        return str(self.certificate)
