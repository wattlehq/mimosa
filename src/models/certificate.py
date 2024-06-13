from django.db import models


class Certificate(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.choice_text
