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

    def test_create_certificate(self):
        # Create a Certificate instance
        certificate = Certificate(
            name="Test Certificate",
            price=Decimal('19.99'),
            description="A test certificate",
            account_code="ACC123"
        )

        certificate.save()

        # Fetch the certificate from the database
        fetched_certificate = Certificate.objects.get(pk=certificate.pk)

        # Assert that the fetched certificate matches the created one
        self.assertEqual(fetched_certificate.name, "Test Certificate")
        self.assertEqual(fetched_certificate.price, Decimal('19.99'))
        self.assertEqual(fetched_certificate.description, "A test certificate")
        self.assertEqual(fetched_certificate.account_code, "ACC123")
