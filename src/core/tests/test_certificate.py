from decimal import Decimal
from unittest.mock import MagicMock
from unittest.mock import call
from unittest.mock import patch

from django.test import TestCase

from app import settings
from core.models.certificate import Certificate


class CertificateModelTest(TestCase):

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

    @patch("stripe.Price.modify")
    @patch("stripe.Price.create")
    def test_update_certificate_price(self, mock_create, mock_modify):
        mock_create.return_value = MagicMock(stripe_id="price_test")

        # Create a Certificate instance
        certificate = Certificate(
            name="Test Certificate",
            price=Decimal("19.99"),
            description="A test certificate",
            account_code="ACC123",
        )

        # Initial save and store.
        certificate.save()
        initial_product_id = certificate.stripe_product_id
        initial_price_id = certificate.stripe_price_id

        # Update the price
        certificate.price = Decimal("29.99")
        certificate.save()

        # Fetch the updated certificate from the database
        updated_certificate = Certificate.objects.get(pk=certificate.pk)

        # Assert the initial price disabled.
        mock_modify.assert_called_once_with(initial_price_id, active=False)

        expected_calls = [
            # Assert the initial price created.
            call(
                product=initial_product_id,
                unit_amount=1999,
                currency=settings.STRIPE_CURRENCY,
            ),
            # Assert the new price created.
            call(
                product=updated_certificate.stripe_product_id,
                unit_amount=2999,
                currency=settings.STRIPE_CURRENCY,
            ),
        ]

        self.assertEqual(mock_create.call_args_list, expected_calls)
