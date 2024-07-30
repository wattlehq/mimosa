from django.conf import settings
from django.core.management.base import BaseCommand

from core.models.order import Order
from core.services.email.send_order_status import send_order_status_email


class Command(BaseCommand):
    """
    Django management command to send a test order status email.

    This command allows sending a test email for a specific order to a
    specified email address. It temporarily changes the order's email,
    sends the test email, and then reverts the email change.

    Usage:
        ./run manage send_test_email <order_id> <email>
    """

    help = "Sends a test order status email"

    def add_arguments(self, parser):
        parser.add_argument("order_id", type=int)
        parser.add_argument("email", type=str)

    def handle(self, *args, **options):
        order_id = options["order_id"]
        test_email = options["email"]

        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f"Order with ID {order_id} does not exist")
            )
            return

        # Temporarily change the order's email to the test email
        original_email = order.customer_email
        order.customer_email = test_email
        order.save()

        # Send the test email
        success = send_order_status_email(order_id)

        # Revert the email change
        order.customer_email = original_email
        order.save()

        if success:
            self.stdout.write(
                self.style.SUCCESS(
                    f"Test email sent successfully to {test_email}"
                )
            )
        else:
            self.stdout.write(self.style.ERROR("Failed to send test email"))

        # Email settings
        self.stdout.write(f"EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
        self.stdout.write(f"EMAIL_HOST: {settings.EMAIL_HOST}")
        self.stdout.write(f"EMAIL_PORT: {settings.EMAIL_PORT}")
        self.stdout.write(f"EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
        self.stdout.write(f"EMAIL_USE_SSL: {settings.EMAIL_USE_SSL}")
