import stripe


def create_stripe_tax_rate(tax_rate):
    try:
        stripe_tax_rate = stripe.TaxRate.create(
            display_name=tax_rate.name,
            description=f"{tax_rate.name} Tax Rate",
            percentage=float(tax_rate.percentage),
            inclusive=False,
            active=tax_rate.is_active,
            metadata={"tax_rate_id": str(tax_rate.id)},
        )
        tax_rate.stripe_tax_rate_id = stripe_tax_rate.id
        tax_rate.save(update_fields=["stripe_tax_rate_id"])
        return True
    except stripe.error.StripeError as e:
        print(f"Stripe error: {str(e)}")
        return False
