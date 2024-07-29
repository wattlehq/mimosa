from django.db import models


class Settings(models.Model):
    logo = models.ImageField(upload_to="logos/", blank=True, null=True)

    def __str__(self):
        return "Settings"

    class Meta:
        verbose_name = "Setting"
        verbose_name_plural = "Settings"
