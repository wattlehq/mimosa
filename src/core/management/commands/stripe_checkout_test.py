from django.core.management.base import BaseCommand
from django.urls import reverse

from core.services.utils.random_order import generate_random_request
from core.services.utils.stripe_service import StripeService

# Input the "lines" value if you aren't using the --random flag
manual_request = {
    "property_id": 1,
    "lines": [{"certificate_id": 1, "fee_id": 1}, {"certificate_id": 2}],
}


def create_line_items():
    line_items = []

    for value in request["lines"]:
        certificate_id = value["certificate_id"]
        certificate = Certificate.objects.get(pk=certificate_id)

        line_items.append(
            {"price": certificate.stripe_price_id, "quantity": 1}
        )

        if "fee_id" in value:
            fee_id = value["fee_id"]
            is_valid_fee = certificate.fees.filter(id=fee_id).exists()
            if is_valid_fee:
                fee = Fee.objects.get(pk=fee_id)
                line_items.append(
                    {"price": fee.stripe_price_id, "quantity": 1}
                )

    return line_items


def create_stripe_checkout_session(order_session: OrderSession):
    line_items = create_line_items()
    return stripe.checkout.Session.create(
        line_items=line_items,
        metadata={"order_session_pk": order_session.id},
        mode="payment",
        success_url=get_site_url() + reverse("order_success"),
        cancel_url=get_site_url() + reverse("order_form"),
    )


def save_order_session():
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


def update_order_session(order_session: OrderSession, stripe_checkout_id: str):
    order_session.stripe_checkout_id = stripe_checkout_id
    order_session.save()


class Command(BaseCommand):
    """
    Django management command to create a Stripe checkout instance for testing.

    This command allows for the creation of a Stripe checkout session with
    either predefined or randomly generated order details.

    """

    help = "Create a Stripe checkout instance"

    def add_arguments(self, parser):
        parser.add_argument(
            "--random",
            action="store_true",
            help="Use random selection of certificates and fees",
        )

    def handle(self, *args, **options):
        """
        Execute the command to create a Stripe checkout instance.

        This method initialises the Stripe service, generates or uses a
        predefined order request, creates an OrderSession, creates a Stripe
        checkout session, and updates the OrderSession with the Stripe
        checkout ID.

        Args:
            *args: Variable length argument list.
            **options: Arbitrary keyword arguments. Includes 'random' flag.

        Raises:
            Exception: For any errors that occur during the process.
        """
        StripeService.initialise()  # Initialise Stripe API key

        if options["random"]:
            request = generate_random_request()
        else:
            request = manual_request

        self.stdout.write(self.style.SUCCESS(f"Generated request: {request}"))

        try:
            order_session = StripeService.save_order_session(request)
            stripe_checkout = StripeService.create_stripe_checkout_session(
                order_session, request
            )
            StripeService.update_order_session(
                order_session, stripe_checkout.stripe_id
            )

            self.stdout.write(
                self.style.SUCCESS(f"Checkout URL: {stripe_checkout.url}")
            )

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An error occurred: {str(e)}"))
