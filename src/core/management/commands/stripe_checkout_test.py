import stripe
from core.services.utils.site import get_site_url
from django.conf import settings
from django.core.management.base import BaseCommand

stripe.api_key = settings.STRIPE_SECRET_KEY


class Command(BaseCommand):
    help = "Create a Stripe checkout instance"

    def handle(self, *args, **kwargs):
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    "price": "price_1PWPoIBEiTiT42p62cyp4UF3",
                    "quantity": 1,
                },
                {
                    "price": "price_1PWPngBEiTiT42p6vNkKOQ5j",
                    "quantity": 1,
                }
            ],
            metadata={
                "property_id": "1",
                "fee__price_1PWPoIBEiTiT42p62cyp4UF3":
                    "price_1PWPngBEiTiT42p6vNkKOQ5j"
            },
            mode="payment",
            success_url=get_site_url() + "/success.html",
            cancel_url=get_site_url() + "/cancel.html",
        )

        self.stdout.write(self.style.SUCCESS(checkout_session.url))
