from decimal import Decimal

import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_API_SECRET_KEY


def sync_to_stripe_new(name_new: str, price_new: Decimal, pk: str):
    stripe_product = stripe.Product.create(
        name=name_new,
        metadata={"certificate_pk": pk}
    )

    price_cents = int(price_new * 100)
    stripe_price = stripe.Price.create(
        product=stripe_product.stripe_id,
        unit_amount=price_cents,  # Stripe expects the amount in cents
        currency=settings.STRIPE_CURRENCY
    )

    return stripe_product.stripe_id, stripe_price.stripe_id


def sync_to_stripe_existing(
        product_id: str,
        price_id: str,
        price_new: Decimal,
        price_old: Decimal,
        name_new: str,
        name_old: str
):
    price_id_new = price_id
    price_new_cents = int(price_new * 100)

    if name_old != name_new:
        stripe.Product.modify(product_id, name=name_new)

    if price_old != price_new:
        stripe.Price.modify(price_id, active=False)

        price_id_new = stripe.Price.create(
            product=product_id,
            unit_amount=price_new_cents,
            currency=settings.STRIPE_CURRENCY
        ).stripe_id

    return product_id, price_id_new
