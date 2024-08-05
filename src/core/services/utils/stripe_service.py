import stripe
from django.conf import settings

from core.models.certificate import Certificate
from core.models.fee import Fee
from core.models.order import OrderSession
from core.models.order import OrderSessionLine
from core.models.property import Property
from core.services.utils.site import get_site_url


class StripeService:
    """
    A service class for handling Stripe-related operations.
    """

    @classmethod
    def initialise(cls):
        stripe.api_key = settings.STRIPE_SECRET_KEY

    @classmethod
    def create_line_items(cls, request):
        """
        Create line items for a Stripe checkout session based on the request.

        Args:
            request: A dictionary containing order details with 'lines' key.

        Returns:
            list: A list of dictionaries, each representing a line item for
                  Stripe checkout.

        Raises:
            ObjectDoesNotExist: If a referenced Certificate or Fee object
                                doesn't exist.
        """
        line_items = []
        for value in request["lines"]:
            certificate_id = value["certificate_id"]
            certificate = Certificate.objects.get(pk=certificate_id)
            line_item = {"price": certificate.stripe_price_id, "quantity": 1}
            if certificate.tax_rate:
                line_item["tax_rates"] = [
                    certificate.tax_rate.stripe_tax_rate_id
                ]
            line_items.append(line_item)

            if "fee_id" in value:
                fee_id = value["fee_id"]
                is_valid_fee = certificate.fees.filter(id=fee_id).exists()
                if is_valid_fee:
                    fee = Fee.objects.get(pk=fee_id)
                    fee_line_item = {
                        "price": fee.stripe_price_id,
                        "quantity": 1,
                    }
                    if fee.tax_rate:
                        fee_line_item["tax_rates"] = [
                            fee.tax_rate.stripe_tax_rate_id
                        ]
                    line_items.append(fee_line_item)
        return line_items

    @classmethod
    def create_stripe_checkout_session(
        cls, order_session: OrderSession, request
    ):
        """
        Create a Stripe checkout session for the given order session and req.

        Args:
            order_session (OrderSession): The OrderSession object for which to
                                          create a checkout.
            request (dict): A dictionary containing order details.

        Returns:
            stripe.checkout.Session: A Stripe checkout session object.

        Raises:
            stripe.error.StripeError: If there's an error creating the Stripe
                                      checkout session.
        """
        line_items = cls.create_line_items(request)
        return stripe.checkout.Session.create(
            line_items=line_items,
            metadata={"order_session_pk": order_session.id},
            mode="payment",
            success_url=get_site_url() + "/success",
            cancel_url=get_site_url() + "/cancel",
        )

    @classmethod
    def save_order_session(cls, request):
        """
        Create and save an OrderSession and associated OrderSessionLines.

        Args:
            request (dict): A dictionary containing order details with
                            'property_id' and 'lines' keys.

        Returns:
            OrderSession: The created and saved OrderSession object.

        Raises:
            ObjectDoesNotExist: If the specified Property, Certificate, or Fee
                                objects don't exist.
        """
        property_obj = Property.objects.get(id=request["property_id"])
        order_session = OrderSession(property=property_obj)
        order_session.save()

        for value in request["lines"]:
            certificate_id = value["certificate_id"]
            certificate = Certificate.objects.get(id=certificate_id)
            order_line = OrderSessionLine.objects.create(
                order_session=order_session,
                certificate=certificate,
                cost_certificate=certificate.price,
            )

            if "fee_id" in value:
                fee_id = value["fee_id"]
                fee = Fee.objects.get(id=fee_id)
                is_valid_fee = certificate.fees.filter(id=fee_id).exists()
                if is_valid_fee:
                    order_line.fee = fee
                    order_line.cost_fee = fee.price
                    order_line.save()

        return order_session

    @classmethod
    def update_order_session(
        cls, order_session: OrderSession, stripe_checkout_id: str
    ):
        """
        Update the given OrderSession with the Stripe checkout ID.

        Args:
            order_session (OrderSession): The OrderSession object to update.
            stripe_checkout_id (str): The Stripe checkout session ID to
                                      associate with the order.
        """
        order_session.stripe_checkout_id = stripe_checkout_id
        order_session.save()
