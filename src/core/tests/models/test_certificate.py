from decimal import Decimal
from unittest.mock import MagicMock
from unittest.mock import patch

from django.test import TestCase

from app import settings
from core.models.certificate import Certificate


class CertificateModelTest(TestCase):

    @patch("stripe.Product.create")
    @patch("stripe.Price.create")
    def test_create_certificate(self, mock_price_create, mock_product_create):
        mock_product_create.return_value = MagicMock(stripe_id="product_test")
        mock_price_create.return_value = MagicMock(stripe_id="price_test")

        # Create a Certificate instance
        certificate = Certificate(
            name="Test Certificate 22",
            price=Decimal("19.99"),
            description="A test certificate",
            account_code="ACC123",
        )

        certificate.save()
        initial_product_id = certificate.stripe_product_id

        # Assert product is created.
        mock_product_create.assert_called_once_with(
            name="Test Certificate 22",
            metadata={"certificate_pk": str(certificate.pk)},
        )

        # Assert price is created.
        mock_price_create.assert_called_once_with(
            product=initial_product_id,
            unit_amount=1999,
            currency=settings.STRIPE_CURRENCY,
        )

        # Assert new IDs are stored.
        self.assertEqual(certificate.stripe_product_id, "product_test")
        self.assertEqual(certificate.stripe_price_id, "price_test")

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
        initial_price_id = certificate.stripe_price_id

        # Update the price
        certificate.price = Decimal("29.99")
        certificate.save()

        # Fetch the updated certificate from the database
        updated_certificate = Certificate.objects.get(pk=certificate.pk)

        # Assert the initial price disabled.
        mock_modify.assert_called_once_with(initial_price_id, active=False)

        # Assert the new price created.
        mock_create.assert_any_call(
            product=updated_certificate.stripe_product_id,
            unit_amount=2999,
            currency=settings.STRIPE_CURRENCY,
        )

        # Assert new IDs are stored.
        self.assertEqual(certificate.stripe_price_id, "price_test")
