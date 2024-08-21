from core.models.tax_rate import TaxRate


def get_active_tax_rate():
    return TaxRate.objects.filter(is_active=True).first()
