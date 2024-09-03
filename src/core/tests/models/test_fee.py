from decimal import Decimal
from unittest.mock import MagicMock
from unittest.mock import patch

from django.test import TestCase

from app import settings
from core.models.fee import Fee
from core.models.tax_rate import TaxRate


class FeeTestCase(TestCase):
    def setUp(self):
        Fee.objects.all().delete()
        TaxRate.objects.all().delete()

    @patch("stripe.Product.create")
    @patch("stripe.Price.create")
    def test_create_fee_stripe_sync(
        self, mock_price_create, mock_product_create
    ):
        mock_product_create.return_value = MagicMock(stripe_id="product_test")
        mock_price_create.return_value = MagicMock(stripe_id="price_test")

        fee = Fee(name="Test Fee", price=Decimal("9.99"))
        fee.save()

        initial_product_id = fee.stripe_product_id

        # Assert product is created.
        mock_product_create.assert_called_once_with(
            name="Test Fee",
            metadata={"fee_pk": str(fee.pk)},
        )

        # Assert price is created.
        mock_price_create.assert_called_once_with(
            product=initial_product_id,
            unit_amount=999,
            currency=settings.STRIPE_CURRENCY,
        )

        # Assert new IDs are stored.
        self.assertEqual(fee.stripe_product_id, "product_test")
        self.assertEqual(fee.stripe_price_id, "price_test")

    @patch("stripe.Price.modify")
    @patch("stripe.Price.create")
    def test_update_fee_price(self, mock_create, mock_modify):
        mock_create.return_value = MagicMock(stripe_id="price_test")

        fee = Fee(name="Test Fee", price=Decimal("9.99"))
        fee.save()
        initial_price_id = fee.stripe_price_id

        # Update the price
        fee.price = Decimal("19.99")
        fee.save()

        # Fetch the updated fee from the database
        updated_fee = Fee.objects.get(pk=fee.pk)

        # Assert the initial price disabled.
        mock_modify.assert_called_once_with(initial_price_id, active=False)

        # Assert the new price created.
        mock_create.assert_any_call(
            product=updated_fee.stripe_product_id,
            unit_amount=1999,
            currency=settings.STRIPE_CURRENCY,
        )

        # Assert new IDs are stored.
        self.assertEqual(fee.stripe_price_id, "price_test")

    @patch("stripe.Product.create")
    @patch("stripe.Price.create")
    def test_add_tax_rate_to_fee(self, mock_price_create, mock_product_create):
        # Mock Stripe responses
        mock_product_create.return_value = MagicMock(stripe_id="product_test")
        mock_price_create.return_value = MagicMock(stripe_id="price_test")

        # Create a Fee without a tax rate
        fee = Fee(name="Test Fee", price=Decimal("9.99"))
        fee.save()

        # Create a TaxRate and add it to the Fee
        tax_rate = TaxRate(
            name="GST", percentage=20.0, stripe_tax_rate_id="txr_test"
        )
        tax_rate.save()
        fee.tax_rate = tax_rate
        fee.save()

        # Assert that the price was updated with the tax rate
        mock_price_create.assert_called_with(
            product=fee.stripe_product_id,
            unit_amount=999,
            currency=settings.STRIPE_CURRENCY,
            tax_behavior="exclusive",
            metadata={"tax_rate": tax_rate.stripe_tax_rate_id},
        )

        # Assert new IDs are stored
        self.assertEqual(fee.stripe_price_id, "price_test")

    @patch("stripe.Price.modify")
    @patch("stripe.Price.create")
    def test_update_fee_tax_rate(self, mock_price_create, mock_price_modify):
        # Mock Stripe responses
        mock_price_create.return_value = MagicMock(stripe_id="new_price_test")

        # Create a TaxRate and a Fee with this tax rate
        initial_tax_rate = TaxRate(
            name="Initial Tax",
            percentage=10.0,
            stripe_tax_rate_id="txr_initial",
        )
        initial_tax_rate.save()
        fee = Fee(
            name="Test Fee", price=Decimal("9.99"), tax_rate=initial_tax_rate
        )
        fee.save()
        initial_price_id = fee.stripe_price_id

        # Create a new TaxRate and update the Fee with this new tax rate
        new_tax_rate = TaxRate(
            name="New Tax", percentage=15.0, stripe_tax_rate_id="txr_new"
        )
        new_tax_rate.save()
        fee.tax_rate = new_tax_rate
        fee.save()

        # Assert the initial price was disabled
        mock_price_modify.assert_called_once_with(
            initial_price_id, active=False
        )

        # Assert the new price was created with the new tax rate
        mock_price_create.assert_called_with(
            product=fee.stripe_product_id,
            unit_amount=999,
            currency=settings.STRIPE_CURRENCY,
            tax_behavior="exclusive",
            metadata={"tax_rate": new_tax_rate.stripe_tax_rate_id},
        )

        # Assert new IDs are stored
        self.assertEqual(fee.stripe_price_id, "new_price_test")
