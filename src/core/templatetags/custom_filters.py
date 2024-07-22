import os

from django import template

register = template.Library()


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
