from core.services.order.send_email_status import send_email_status


def admin_send_email_status(modeladmin, request, queryset):
    for order in queryset:
        send_email_status(order.pk)

    modeladmin.message_user(
        request, "Email sent successfully to selected customers."
    )


admin_send_email_status.short_description = "Send order status email"
