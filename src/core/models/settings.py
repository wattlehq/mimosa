from django.core.cache import cache
from django.core.validators import EmailValidator
from django.db import models


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

        # Clear the cache
        cache.delete("app_settings")

        # Update the cache with new values
        cache.set("app_settings", self, timeout=3600)

    class Meta:
        verbose_name = "Setting"
        verbose_name_plural = "Settings"
