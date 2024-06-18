from django.db import models
from django.utils import timezone

from .certificate import Certificate
from .property import Property


class Order(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_fulfilled = models.BooleanField(default=False)

    customer_email = models.EmailField(max_length=254)
    customer_phone = models.CharField(max_length=15, null=True)
    customer_mobile = models.CharField(max_length=15, null=True)
    customer_company_name = models.CharField(max_length=200, null=True)
    customer_company_ref = models.CharField(max_length=200, null=True)
    customer_address_street_line_1 = models.CharField(max_length=200, null=True)
    customer_address_street_line_2 = models.CharField(max_length=200, null=True)
    customer_address_suburb = models.CharField(max_length=50, null=True)
    customer_address_state = models.CharField(max_length=3, null=True)
    customer_address_post_code = models.CharField(max_length=4, null=True)

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


def certificate_file_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/certificates/order_<id>/<filename>
    return "certificates/order_{0}/{1}".format(instance.certificate.id,
                                               filename)


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
        upload_to=certificate_file_directory_path, null=True)

    def __str__(self):
        return str(self.certificate)
