# Generated by Django 5.0.3 on 2024-07-02 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0005_fee_created_at_fee_price_fee_stripe_price_id_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="order",
            name="customer_mobile",
        ),
        migrations.AddField(
            model_name="order",
            name="customer_address_country",
            field=models.CharField(max_length=3, null=True),
        ),
    ]
