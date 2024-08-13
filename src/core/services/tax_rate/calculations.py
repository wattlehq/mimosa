from core.models.tax_rate import TaxRate


def calculate_cost_with_tax(amount: float, tax_rate: TaxRate) -> float:
    """Calculate tax amount based on the given amount and tax rate."""
    if tax_rate is None or tax_rate == 0:
        return amount
    return amount * (tax_rate.percentage / 100)
