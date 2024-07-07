import stripe
from django.conf import settings
from django.core.management.base import BaseCommand

from core.models.certificate import Certificate
from core.models.fee import Fee
from core.models.order import OrderSession, OrderSessionLine
from core.models.property import Property
from core.services.utils.site import get_site_url

stripe.api_key = settings.STRIPE_SECRET_KEY

request = {
    "property_id": 1,
    "lines": [
        {
            "certificate_id": 1,
            "fee_id": 3
        },
        {
            "certificate_id": 2
        }
    ]
}


def create_line_items():
    line_items = []

    for value in request["lines"]:
        certificate_id = value["certificate_id"]
        certificate = Certificate.objects.get(pk=certificate_id)

        line_items.append({
            "price": certificate.stripe_price_id,
            "quantity": 1
        })

        if "fee_id" in value:
            fee_id = value["fee_id"]
            is_valid_fee = certificate.fees.filter(id=fee_id).exists()
            if is_valid_fee:
                fee = Fee.objects.get(pk=fee_id)
                line_items.append({
                    "price": fee.stripe_price_id,
                    "quantity": 1
                })

    return line_items


def create_stripe_order_session():
    line_items = create_line_items()
    return stripe.checkout.Session.create(
        line_items=line_items,
        mode="payment",
        success_url=get_site_url() + "/success.html",
        cancel_url=get_site_url() + "/cancel.html",
    )


def save_order_session(session_id: str):
    property_obj = Property.objects.get(id=request["property_id"])

    order_session = OrderSession(
        property=property_obj,
        stripe_session_id=session_id,
    )

    order_session.save()

    for value in request["lines"]:
        certificate_id = value["certificate_id"]
        certificate = Certificate.objects.get(id=certificate_id)
        order_line = OrderSessionLine.objects.create(
            order_session=order_session,
            certificate=certificate
        )

        if "fee_id" in value:
            fee_id = value["fee_id"]
            fee = Fee.objects.get(id=fee_id)
            is_valid_fee = certificate.fees.filter(id=fee_id).exists()
            if is_valid_fee:
                order_line.fee = fee
                order_line.save()


class Command(BaseCommand):
    help = "Create a Stripe checkout instance"

    def handle(self, *args, **kwargs):
        session = create_stripe_order_session()
        save_order_session(session.stripe_id)
        self.stdout.write(self.style.SUCCESS(session.url))
