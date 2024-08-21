from decimal import Decimal

import stripe
from django.test import TestCase

from core.models.certificate import Certificate


class CertificateModelTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Set the API base URL to stripe-mock
        stripe.api_key = "sk_test_123"
        stripe.api_base = "http://stripe-mock:12111"
        print(f"Stripe API base set to: {stripe.api_base}")

    def test_create_certificate(self):
        # Create a Certificate instance
        certificate = Certificate(
            name="Test Certificate 22",
            price=Decimal("19.99"),
            description="A test certificate",
            account_code="ACC123",
        )

        certificate.save()

        # Fetch the certificate from the database
        fetched_certificate = Certificate.objects.get(pk=certificate.pk)

        # Assert that the fetched certificate matches the created one
        self.assertEqual(fetched_certificate.name, "Test Certificate 22")
        self.assertEqual(fetched_certificate.price, Decimal("19.99"))
        self.assertEqual(fetched_certificate.description, "A test certificate")
        self.assertEqual(fetched_certificate.account_code, "ACC123")

    def test_update_certificate_price(self):
        # Create a Certificate instance
        certificate = Certificate(
            name="Test Certificate",
            price=Decimal("19.99"),
            description="A test certificate",
            account_code="ACC123",
        )
        certificate.save()
        print(f"Created certificate: {certificate.name}, ID: {certificate.id}")
        print(f"Initial Stripe Product ID: {certificate.stripe_product_id}")
        print(f"Initial Stripe Price ID: {certificate.stripe_price_id}")

        # Update the price
        certificate.price = Decimal("29.99")
        certificate.save()
        print(f"Updated certificate price to: {certificate.price}")

        # Fetch the updated certificate from the database
        updated_certificate = Certificate.objects.get(pk=certificate.pk)
        print(
            f"Fetched updated certificate: {updated_certificate.name}, ID: {updated_certificate.id}"
        )
        print(
            f"Updated Stripe Product ID: {updated_certificate.stripe_product_id}"
        )
        print(
            f"Updated Stripe Price ID: {updated_certificate.stripe_price_id}"
        )

        # Assert that the updated certificate matches the new price
        self.assertEqual(updated_certificate.price, Decimal("29.99"))

        # Verify the price update in Stripe
        stripe_product = stripe.Product.retrieve(
            updated_certificate.stripe_product_id
        )
        stripe_price = stripe.Price.retrieve(
            updated_certificate.stripe_price_id
        )

        # Debug: Print the retrieved product name and price
        print(f"Retrieved Stripe Product Name: {stripe_product.name}")
        print(f"Retrieved Stripe Price Amount: {stripe_price.unit_amount}")

        self.assertEqual(stripe_product.name, "Test Certificate")
        self.assertEqual(
            stripe_price.unit_amount, 2999
        )  # Stripe expects the amount in cents
