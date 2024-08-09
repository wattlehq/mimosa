from django.core.management.base import BaseCommand

from core.services.order.create_order_session import create_order_session
from core.services.test.generate_random_order import generate_random_order

manual_request = {
    "property_id": 1,
    "order_lines": [
        {"certificate_id": 13, "fee_id": 1},
        {"certificate_id": 12},
    ],
    "customer_name": "Vitalik Buterin",
    "customer_company_name": "ETH Inc.",
}


class Command(BaseCommand):
    help = "Create a Stripe checkout instance"

    def add_arguments(self, parser):
        parser.add_argument(
            "--random",
            action="store_true",
            help="Use random selection of certificates and fees",
        )

    def handle(self, *args, **options):
        if options["random"]:
            request = generate_random_order()
        else:
            request = manual_request

        self.stdout.write(self.style.SUCCESS(f"Generated request: {request}"))

        try:
            result = create_order_session(
                property_id=request["property_id"],
                order_lines=request["order_lines"],
                customer_name=request["customer_name"],
                customer_company_name=request["customer_company_name"],
            )

            if result["success"]:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Checkout URL: {result['checkout_url']}"
                    )
                )
            else:
                self.stdout.write(
                    self.style.ERROR(f"Error: {result['error']}")
                )

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An error occurred: {str(e)}"))
