import stripe
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from core.models.certificate import Certificate
from core.models.order import Order, OrderLine
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


# @todo Validate that all prices and PKs exist.
# @todo Validate that fee can be allocated to certificate on order create.
def handle_stripe_checkout_session_completed(event: stripe.checkout.Session):
    event_data = event
    property_id = event_data.metadata.property_id
    property_obj = Property.objects.get(id=property_id)

    # Expand product data for product metadata.
    line_items_data = stripe.checkout.Session.retrieve(
        event_data["id"],
        expand=["line_items", "line_items.data.price.product"],
    )

    line_items = line_items_data["line_items"]

    certificates = {}
    fees = {}

    # @todo Move this mapping to a function.
    for item in line_items["data"]:
        price = item["price"]
        price_id = price["id"]
        product_id = price["product"]["id"]
        metadata = price["product"]["metadata"]

        if "certificate_pk" in metadata:
            certificate_pk = metadata["certificate_pk"]
            certificates[price_id] = {
                "price": price_id,
                "product": product_id,
                "certificate_pk": certificate_pk
            }

        if "fee_pk" in metadata:
            fee_pk = metadata["fee_pk"]
            fees[price_id] = {
                "price": price_id,
                "product": product_id,
                "fee_pk": fee_pk,
            }

    for key, value in event_data.metadata.items():
        if key.startswith("fee__"):
            [fee_key, fee_price] = key.split("__")
            if fee_key == "fee" and value in certificates and fee_price in fees:
                certificates[value]["fee"] = fees[fee_price]

    # @todo Move all the saving logic below to a function.
    # @todo Maybe do this in a transaction to prevent failure?
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

    # @todo Implement fee FK
    for key, value in certificates.items():
        certificate = Certificate.objects.get(id=value["certificate_pk"])
        OrderLine.objects.create(
            order=order,
            certificate=certificate
        )
