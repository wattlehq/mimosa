import stripe
from django.conf import settings
from django.db import transaction
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from core.models.order import Order
from core.models.order import OrderLine
from core.models.order import OrderSession
from core.models.order import OrderSessionLine
from core.models.order import OrderSessionStatus
from core.models.property import Property

stripe.api_key = settings.STRIPE_SECRET_KEY
endpoint_secret = settings.STRIPE_WEBHOOK_SECRET


@csrf_exempt
def webhook_stripe(request):
    payload = request.body
    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]

    try:
        # Verify the webhook signature
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        # Invalid signature
        return HttpResponse(status=400)

    if event["type"] == "checkout.session.completed":
        event_data = event["data"]["object"]
        handle_stripe_checkout_session_completed(event_data)

    else:
        # Unexpected event type
        return HttpResponse(status=400)

    return HttpResponse(status=200)


# Creates an order instance from a Stripe Checkout Session.
@transaction.atomic
def save_event_order(event: stripe.checkout.Session):
    order_session_id = event.metadata["order_session_pk"]
    order_session = OrderSession.objects.get(id=order_session_id)
    property_obj = Property.objects.get(id=order_session.property_id)
    customer = event.customer_details

    order = Order(
        customer_name=order_session.customer_name,
        customer_company_name=order_session.customer_company_name,
        customer_email=customer.email,
        customer_phone=customer.phone,
        customer_address_street_line_1=customer.address.line1,
        customer_address_street_line_2=customer.address.line2,
        customer_address_suburb=customer.address.city,
        customer_address_state=customer.address.state,
        customer_address_post_code=customer.address.postal_code,
        customer_address_country=customer.address.state,
        property=property_obj,
        order_session=order_session,
        stripe_payment_intent=event.payment_intent,
    )

    order.save()
    order_session_lines = OrderSessionLine.objects.filter(
        order_session=order_session.pk
    )

    for session_order_line in order_session_lines:
        # Save certificate to order line.
        order_line = OrderLine.objects.create(
            order=order,
            certificate=session_order_line.certificate,
            fee=session_order_line.fee,
            cost_certificate=session_order_line.cost_certificate,
            cost_fee=session_order_line.cost_fee,
        )

        order_line.save()

    order_session.status = OrderSessionStatus.COMPLETED
    order_session.save()


def save_event_order_error(event: stripe.checkout.Session, e: Exception):
    order_session_id = event.metadata["order_session_pk"]
    order_session = OrderSession.objects.get(id=order_session_id)
    order_session.status_error = str(e)
    order_session.status = OrderSessionStatus.ERROR
    order_session.save()


# Creates an order instance from a certificate and fee PK map.
def handle_stripe_checkout_session_completed(event: stripe.checkout.Session):
    try:
        save_event_order(event)
    except Exception as e:
        save_event_order_error(event, e)
