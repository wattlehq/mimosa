import json
from decimal import Decimal
from unittest.mock import MagicMock
from unittest.mock import patch

from django.test import TestCase

from core.models.certificate import Certificate
from core.models.property import Property
from core.services.order.create_order_session import create_order_session
from core.webhooks.stripe import handle_stripe_checkout_session_completed


class OrderModelTest(TestCase):

    @patch("core.webhooks.stripe.send_email_status")
    @patch("stripe.Product.create")
    @patch("stripe.Price.create")
    def test_create_certificate(
        self, mock_price_create, mock_product_create, mock_email
    ):
        mock_product_create.return_value = MagicMock(stripe_id="product_test")
        mock_price_create.return_value = MagicMock(stripe_id="price_test")

        with open(
            "./core/tests/data/stripe_checkout_session_complete.json"
        ) as json_file:
            event = json.load(json_file)

        prop = Property(
            assessment="10",
            lot="100",
            section="1000",
            deposited_plan="2000",
            address_state="NSW",
            address_suburb="Faketown",
            address_street="123 Fake St",
            address_post_code="2000",
        )

        prop.save()

        certificate = Certificate(
            name="Test Certificate",
            price=Decimal("20.00"),
            description="A test certificate",
            account_code="ACC123",
        )

        certificate.save()

        order_session = create_order_session(
            property_id=prop.pk,
            order_lines=[{"certificate_id": certificate.pk}],
            customer_name="John Doe",
            customer_company_name="Commins Hendricks",
        )["order_session"]

        certificate.save()

        event_data = event["data"]["object"]
        order = handle_stripe_checkout_session_completed(event_data)

        # Assert metadata has been loaded from metadata and embedded.
        self.assertEqual(order.order_session.pk, order_session.pk)
        self.assertEqual(order.property.pk, prop.pk)
        self.assertEqual(order.orderline_set.all().count(), 1)

        # Assert Stripe data is embedded.
        self.assertEqual(order.customer_name, "John Doe")
        self.assertEqual(order.customer_email, "john@example.com")
        self.assertEqual(
            order.stripe_payment_intent, "pi_3PrnOyBEiTiT42p6059j9f0h"
        )

        # Assert email is sent.
        mock_email.assert_called_once()
