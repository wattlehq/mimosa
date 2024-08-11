# src/core/models/certificate_bundle.py

from django.db import models
from core.models.certificate import Certificate

class CertificateBundle(models.Model):
    parent_certificate = models.ForeignKey(
        Certificate,
        related_name='parent_bundles',
        on_delete=models.CASCADE
    )
    child_certificate = models.ForeignKey(
        Certificate,
        related_name='child_bundles',
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ('parent_certificate', 'child_certificate')

    def __str__(self):
        return f"{self.parent_certificate.name} includes {self.child_certificate.name}"
