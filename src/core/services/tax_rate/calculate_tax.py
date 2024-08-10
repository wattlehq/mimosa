from core.models.tax_rate import TaxRate


def calculate_tax(amount: float, tax_rate: TaxRate) -> float:
    """Calculate tax amount based on the given amount and tax rate."""
    return amount * (tax_rate.percentage / 100)
