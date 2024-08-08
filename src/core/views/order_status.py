import os

from django import get_version
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.shortcuts import render

from core.models.order import Order
from core.models.order import OrderLine


def order_status(request, order_hash):
    order_obj = get_object_or_404(Order, order_hash=order_hash)
    order_lines = OrderLine.objects.filter(order=order_obj.pk)

    context = {
        "debug": settings.DEBUG,
        "django_ver": get_version(),
        "python_ver": os.environ["PYTHON_VERSION"],
        "order": order_obj,
        "order_lines": order_lines,
    }

    return render(request, "pages/order_status.html", context)
