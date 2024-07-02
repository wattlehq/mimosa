import stripe
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from core.models.order import Order
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


def handle_stripe_checkout_session_completed(event: stripe.checkout.Session):
    event_data = event
    property_id = event_data.metadata.property_id
    property_obj = Property.objects.get(id=property_id)

    # @todo Get types working?
    order = Order(
        customer_email=event_data.customer_details.email,
        customer_phone=event_data.customer_details.phone,
        customer_address_street_line_1=event_data.customer_details.address.line1,
        customer_address_street_line_2=event_data.customer_details.address.line2,
        customer_address_suburb=event_data.customer_details.address.city,
        customer_address_state=event_data.customer_details.address.state,
        customer_address_post_code=event_data.customer_details.address.postal_code,
        customer_address_country=event_data.customer_details.address.state,
        property=property_obj
    )

    order.save()
