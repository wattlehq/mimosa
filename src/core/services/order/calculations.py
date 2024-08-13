from decimal import Decimal


def calculate_order_subtotal(order):
    return sum(
        line.cost_certificate + (line.cost_fee or Decimal("0.00"))
        for line in order.orderline_set.all()
    )


def calculate_order_tax(order):
    return sum(
        (line.tax_amount_certificate or Decimal("0.00"))
        + (line.tax_amount_fee or Decimal("0.00"))
        for line in order.orderline_set.all()
    )


def calculate_order_total(order):
    return calculate_order_subtotal(order) + calculate_order_tax(order)
