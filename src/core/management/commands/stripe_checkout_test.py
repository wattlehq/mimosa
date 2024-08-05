from django.core.management.base import BaseCommand

from core.services.utils.stripe_service import StripeService
from core.services.utils.random_order import generate_random_request

# Input the "lines" value if you aren't using the --random flag
manual_request = {
    "property_id": 1,
    "lines": [{"certificate_id": 1, "fee_id": 1}, {"certificate_id": 2}],
}


class Command(BaseCommand):
    """
    Django management command to create a Stripe checkout instance for testing.

    This command allows for the creation of a Stripe checkout session with
    either predefined or randomly generated order details.

    """
    help = "Create a Stripe checkout instance"

    def add_arguments(self, parser):
        parser.add_argument(
            '--random',
            action='store_true',
            help='Use random selection of certificates and fees',
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

        if options['random']:
            request = generate_random_request()
        else:
            request = manual_request

        self.stdout.write(self.style.SUCCESS(f"Generated request: {request}"))

        try:
            order_session = StripeService.save_order_session(request)
            stripe_checkout = StripeService.create_stripe_checkout_session(
                order_session,
                request
            )
            StripeService.update_order_session(
                order_session,
                stripe_checkout.stripe_id
            )

            self.stdout.write(self.style.SUCCESS(
                f"Checkout URL: {stripe_checkout.url}")
            )

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An error occurred: {str(e)}"))
