import stripe


def create_stripe_tax_rate(tax_rate):
    stripe_tax_rate = stripe.TaxRate.create(
        display_name=tax_rate.name,
        description=f"{tax_rate.name} Tax Rate",
        percentage=float(tax_rate.percentage),
        inclusive=False,  # Assuming tax is not included in the price
        active=tax_rate.is_active,
        metadata={"tax_rate_id": str(tax_rate.id)},
    )
    tax_rate.stripe_tax_rate_id = stripe_tax_rate.id
    tax_rate.save()
