import stripe

from django.conf import settings
from django.core.management.base import BaseCommand

stripe.api_key = settings.STRIPE_SECRET_KEY


class Command(BaseCommand):
    help = "Create a Stripe checkout instance"

    def handle(self, *args, **kwargs):
        site_url = settings.SITE_PROTOCOL + settings.SITE_DOMAIN + ":" + str(
            settings.SITE_PORT)
        print(site_url)
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    "price": "price_1PW38VBEiTiT42p6WYrlSD0g",
                    "quantity": 1,
                },
            ],
            mode="payment",
            success_url=site_url + "/success.html",
            cancel_url=site_url + "/cancel.html",
        )

        self.stdout.write(
            self.style.SUCCESS(checkout_session.url))
