import logging

from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse

from core.models.order import Order
from core.services.settings.get_settings import get_settings
from core.services.utils.site import get_site_url

logger = logging.getLogger(__name__)


def send_order_status_email(order_id, override_email=None):
    """
    Send an order status update email to the customer.

    Args:
        order_id (int): The ID of the order to send the status update.

    Returns:
        bool: True if the email was sent successfully, False otherwise.

    Raises:
        ObjectDoesNotExist: If the order with the given ID is not found.
        Exception: For any other errors that occur during the process.

    Logs:
        - Error if the council email is not set in Settings.
        - Info when the email is sent successfully.
        - Error if the order is not found.
        - Exception details for any other errors.
    """
    try:
        # Retrieve the order and its related items
        order = (
            Order.objects.select_related("property")
            .prefetch_related("orderline_set__certificate")
            .get(id=order_id)
        )

        try:
            settings = get_settings()
            council_email = settings.council_email
            if not council_email:
                logger.error(
                    f"Council email not set in Settings for order {order_id}"
                )
                return False
        except ValueError as e:
            logger.error(f"Error retrieving settings: {str(e)}")
            return False

        # reverse() for dynamic paths based on the URL configuration
        order_url = get_site_url() + reverse(
            "order_status", kwargs={"order_hash": str(order.order_hash)}
        )

        # Prepare lists for ready and pending certificates
        order_lines = list(order.orderline_set.all())
        for line in order_lines:
            # Calculate GST and total for each line
            line.gst = (line.tax_amount_certificate or 0) + (
                line.tax_amount_fee or 0
            )
            line.total = (
                (line.cost_certificate or 0) + (line.cost_fee or 0) + line.gst
            )

        ready_certificates = [
            line for line in order_lines if line.is_fulfilled
        ]
        pending_certificates = [
            line for line in order_lines if not line.is_fulfilled
        ]

        # Prepare context for email template
        context = {
            "order": order,
            "order_lines": order_lines,
            "ready_certificates": ready_certificates,
            "pending_certificates": pending_certificates,
            "order_url": order_url,
        }

        # Render email content
        email_subject = f"Order Update - #{order.id}"
        email_body = render_to_string(
            "emails/order_status_update.html", context
        )

        recipient_email = override_email or order.customer_email

        # Send email
        send_mail(
            subject=email_subject,
            message=f"Order update - view it here: {order_url}",
            from_email=council_email,
            recipient_list=[recipient_email],
            html_message=email_body,
            fail_silently=False,
        )

        logger.info(f"Email update sent successfully for order {order_id}")
        return True

    except ObjectDoesNotExist:
        logger.error(f"Order with id {order_id} not found")
        return False
    except Exception as e:
        logger.exception(f"Error sending email for order {order_id}: {str(e)}")
        return False
