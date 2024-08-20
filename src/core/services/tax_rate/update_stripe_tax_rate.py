import stripe

from core.services.tax_rate.create_stripe_tax_rate import (
    create_stripe_tax_rate,
)


def update_stripe_tax_rate(tax_rate):
    if not tax_rate.stripe_tax_rate_id:
        return create_stripe_tax_rate(tax_rate)

    try:
        stripe.TaxRate.modify(
            tax_rate.stripe_tax_rate_id,
            active=tax_rate.is_active,
            metadata={"tax_rate_id": str(tax_rate.id)},
        )
        return True
    except stripe.error.StripeError as e:
        print(f"Stripe error: {str(e)}")
        return False
