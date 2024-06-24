import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_API_SECRET_KEY


def sync_to_stripe_new(**kwargs):
    name_new = kwargs.get("name_new")
    price_new = kwargs.get("price_new")

    # @todo save PK to product.
    stripe_product = stripe.Product.create(name=name_new)
    price_cents = int(price_new * 100)

    stripe_price = stripe.Price.create(
        product=stripe_product.stripe_id,
        unit_amount=price_cents,  # Stripe expects the amount in cents
        currency=settings.STRIPE_CURRENCY
    )

    return stripe_product.stripe_id, stripe_price.stripe_id


def sync_to_stripe_existing(**kwargs):
    stripe_product_id = kwargs.get("product_id")
    stripe_price_id_old = kwargs.get("price_id")
    stripe_price_id_new = stripe_price_id_old

    price_new = kwargs.get("price_new")
    price_old = kwargs.get("price_old")

    name_new = kwargs.get("name_new")
    name_old = kwargs.get("name_old")

    price_new_cents = int(price_new * 100)

    if name_old != name_new:
        stripe.Product.modify(stripe_product_id, name=name_new)

    if price_old != price_new:
        stripe.Price.modify(stripe_price_id_old, active=False)

        stripe_price_id_new = stripe.Price.create(
            product=stripe_product_id,
            unit_amount=price_new_cents,
            currency=settings.STRIPE_CURRENCY
        ).stripe_id

    return stripe_product_id, stripe_price_id_new
