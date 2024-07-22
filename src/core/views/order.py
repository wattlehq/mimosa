import os

from django import get_version
from django.conf import settings
from django.shortcuts import render, get_object_or_404

from core.models.order import Order, OrderLine


def order(request, order_id):
    order_obj = get_object_or_404(Order, id=order_id)

    order_lines = OrderLine.objects.filter(
        order=order_obj.pk
    )

    context = {
        "debug": settings.DEBUG,
        "django_ver": get_version(),
        "python_ver": os.environ["PYTHON_VERSION"],
        "order": order_obj,
        "order_lines": order_lines
    }

    return render(request, "pages/order.html", context)
