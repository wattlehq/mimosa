from decimal import Decimal
from unittest.mock import MagicMock
from unittest.mock import patch

from django.test import TestCase

from app import settings
from core.models.certificate import Certificate
from core.models.tax_rate import TaxRate


class StripeProductTaxRateTestCase(TestCase):
    def setUp(self):
        Certificate.objects.all().delete()
        TaxRate.objects.all().delete()

    @patch("stripe.Product.create")
    @patch("stripe.Price.create")
    def test_add_tax_rate_to_certificate(
        self, mock_price_create, mock_product_create
    ):
        # Mock Stripe responses
        mock_product_create.return_value = MagicMock(stripe_id="product_test")
        mock_price_create.return_value = MagicMock(stripe_id="price_test")

        # Create a Certificate without a tax rate
        certificate = Certificate(
            name="Test Certificate",
            price=Decimal("19.99"),
            description="A test certificate",
            account_code="ACC123",
        )
        certificate.save()

        # Create a TaxRate instance and save it
        tax_rate = TaxRate(
            name="GST", percentage=20.0, stripe_tax_rate_id="txr_test"
        )
        tax_rate.save()

        # Add the tax rate to the Certificate
        certificate.tax_rate = tax_rate
        certificate.save()

        # Assert that the price was updated with the tax rate
        mock_price_create.assert_called_with(
            product=certificate.stripe_product_id,
            unit_amount=1999,
            currency=settings.STRIPE_CURRENCY,
            tax_behavior="exclusive",
            metadata={"tax_rate": tax_rate.stripe_tax_rate_id},
        )

        # Assert new IDs are stored
        self.assertEqual(certificate.stripe_price_id, "price_test")

    @patch("stripe.Price.modify")
    @patch("stripe.Price.create")
    def test_change_certificate_tax_rate(
        self, mock_price_create, mock_price_modify
    ):
        # Mock Stripe responses
        mock_price_create.return_value = MagicMock(stripe_id="new_price_test")

        # Create a TaxRate instance and save it
        initial_tax_rate = TaxRate(
            name="Initial Tax",
            percentage=10.0,
            stripe_tax_rate_id="txr_initial",
        )
        initial_tax_rate.save()

        # Create a Certificate with the initial tax rate
        certificate = Certificate(
            name="Test Certificate",
            price=Decimal("19.99"),
            description="A test certificate",
            account_code="ACC123",
            tax_rate=initial_tax_rate,
        )
        certificate.save()
        initial_price_id = certificate.stripe_price_id

        # Create a new TaxRate instance and save it
        new_tax_rate = TaxRate(
            name="New Tax", percentage=15.0, stripe_tax_rate_id="txr_new"
        )
        new_tax_rate.save()

        # Update the Certificate with the new tax rate
        certificate.tax_rate = new_tax_rate
        certificate.save()

        # Assert the initial price was disabled
        mock_price_modify.assert_called_once_with(
            initial_price_id, active=False
        )

        # Assert the new price was created with the new tax rate
        mock_price_create.assert_called_with(
            product=certificate.stripe_product_id,
            unit_amount=1999,
            currency=settings.STRIPE_CURRENCY,
            tax_behavior="exclusive",
            metadata={"tax_rate": new_tax_rate.stripe_tax_rate_id},
        )

        # Assert new IDs are stored
        self.assertEqual(certificate.stripe_price_id, "new_price_test")
