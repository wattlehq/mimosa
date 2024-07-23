import os
from decimal import Decimal

from django import template

register = template.Library()


@register.filter
def add_decimals(value1, value2):
    """ add two decimal numbers """
    try:
        # check for empty values.
        if value1 is None and value2 is None:
            return 0
        if value1 is None:
            return value2
        if value2 is None:
            return value1

        return Decimal(value1) + Decimal(value2)
    except (TypeError, ValueError):
        return ''


@register.filter
def filesize_kb(value):
    """ converts from bytes to kb """
    try:
        return value / 1024  # Convert bytes to KB
    except (TypeError, AttributeError):
        return None


@register.filter
def filename(value):
    """ converts path/to/file.pdf to file.pdf """
    try:
        return os.path.basename(value)
    except (TypeError, AttributeError):
        return None


@register.filter
def money(value: Decimal | None):
    """ format a decimal value as money """
    try:
        if not value:
            return ""

        formatted_value = "${:,.2f}".format(
            Decimal(value)
        )

        return formatted_value
    except (TypeError, AttributeError):
        return None
