# Generated by Django 5.0.3 on 2024-07-08 22:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0017_alter_ordersession_status_error"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="stripe_payment_intent",
            field=models.CharField(default="pi_123", max_length=254),
            preserve_default=False,
        ),
    ]
