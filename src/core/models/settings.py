from django.core.validators import EmailValidator
from django.db import models

from core.services.settings.cache import SettingsCache


class Settings(models.Model):
    logo = models.ImageField(upload_to="logos/", blank=True, null=True)
    council_email = models.EmailField(
        max_length=254,
        blank=True,
        null=True,
        validators=[EmailValidator()],
        help_text="Email for sending customers order notifications",
    )

    def __str__(self):
        return "Settings"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        SettingsCache.invalidate()
        SettingsCache.update(self)

    class Meta:
        verbose_name = "Setting"
        verbose_name_plural = "Settings"
