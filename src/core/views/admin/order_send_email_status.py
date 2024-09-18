from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect

from core.models.order import Order
from core.services.order.send_email_status import send_email_status


def order_send_email_status(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    send_email_status(order.pk)
    messages.success(request, "Email sent to customer.")
    return redirect(f"/admin/core/order/{order_id}/change/")
