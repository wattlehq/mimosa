from django.contrib import admin

from .models.certificate import Certificate
from .models.fee import Fee
from .models.order import Order, OrderLine
from .models.property import Property


class OrderLineInline(admin.TabularInline):
    model = OrderLine
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderLineInline]
    # @todo Remove email
    exclude = ("email",)


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    exclude = ("stripe_product_id", "stripe_price_id",)


admin.site.register(Property)
admin.site.register(Fee)
