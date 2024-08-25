import json
from decimal import Decimal
from unittest.mock import MagicMock
from unittest.mock import patch

from django.test import TestCase

from core.models.certificate import Certificate
from core.models.order import Order
from core.models.property import Property
from core.services.order.create_order_session import create_order_session
from core.webhooks.stripe import handle_stripe_checkout_session_completed


class OrderModelTest(TestCase):
    @patch("stripe.Product.create")
    @patch("stripe.Price.create")
    def test_create_certificate(self, mock_price_create, mock_product_create):
        mock_product_create.return_value = MagicMock(stripe_id="product_test")
        mock_price_create.return_value = MagicMock(stripe_id="price_test")

        with open(
            "./core/tests/data/stripe_checkout_session_complete.json"
        ) as json_file:
            event = json.load(json_file)

        property = Property(
            assessment="10",
            lot="100",
            section="1000",
            deposited_plan="2000",
            address_state="NSW",
            address_suburb="Faketown",
            address_street="123 Fake St",
            address_post_code="2000"
        )

        property.save()

        certificate = Certificate(
            name="Test Certificate",
            price=Decimal("20.00"),
            description="A test certificate",
            account_code="ACC123",
        )

        certificate.save()

        create_order_session(
            property_id=property.pk,
            order_lines=[{"certificate_id": certificate.pk}],
            customer_name="John Doe",
            customer_company_name="Commins Hendricks",
        )

        certificate.save()

        event_data = event["data"]["object"]
        handle_stripe_checkout_session_completed(event_data)

        order = Order.objects.get(pk=1)

        self.assertEqual(order.customer_name, "John Doe")
