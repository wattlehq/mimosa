import stripe


def update_stripe_tax_rate(tax_rate):
    stripe.TaxRate.modify(
        tax_rate.stripe_tax_rate_id,
        active=tax_rate.is_active,
        metadata={"tax_rate_id": str(tax_rate.id)},
    )
