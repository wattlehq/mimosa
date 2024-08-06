import stripe

from core.models.certificate import Certificate
from core.models.fee import Fee
from core.models.order import OrderSession
from core.models.order import OrderSessionLine
from core.models.property import Property
from core.services.utils.site import get_site_url


def create_order_session(property_id, order_lines):
    try:
        property_obj = Property.objects.get(id=property_id)
        order_session = OrderSession(property=property_obj)
        order_session.save()

        line_items = []

        for item in order_lines:
            certificate = Certificate.objects.get(id=item["certificate_id"])
            order_line = OrderSessionLine.objects.create(
                order_session=order_session,
                certificate=certificate,
                cost_certificate=certificate.price,
            )
            line_items.append(
                {"price": certificate.stripe_price_id, "quantity": 1}
            )

            if item.get("fee_id"):
                fee = Fee.objects.get(id=item["fee_id"])
                order_line.fee = fee
                order_line.cost_fee = fee.price
                order_line.save()
                line_items.append(
                    {"price": fee.stripe_price_id, "quantity": 1}
                )

        stripe_checkout = stripe.checkout.Session.create(
            line_items=line_items,
            metadata={"order_session_pk": order_session.id},
            mode="payment",
            success_url=get_site_url() + "/success",
            cancel_url=get_site_url() + "/cancel",
        )

        order_session.stripe_checkout_id = stripe_checkout.id
        order_session.save()

        return {"success": True, "checkout_url": stripe_checkout.url}
    except Exception as e:
        return {"success": False, "error": str(e)}
