from django.core.exceptions import ValidationError
from django.forms import ModelForm

from core.models.certificate import Certificate


class CertificateAdminForm(ModelForm):
    class Meta:
        model = Certificate
        fields = "__all__"

    def clean(self):
        cleaned_data = super().clean()
        child_certificates = cleaned_data.get("child_certificates")

        if self.instance.pk:
            if (
                self.instance.parent_certificates.exists()
                and child_certificates
            ):
                raise ValidationError(
                    "A certificate with a parent cannot have children."
                )

            for child in child_certificates:
                if child.child_certificates.exists():
                    raise ValidationError(
                        f"The certificate '{child}' already has children "
                        f"and cannot be added as a child."
                    )

        return cleaned_data
