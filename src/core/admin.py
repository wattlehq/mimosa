from django.contrib import admin

from .models.certificate import Certificate
from .models.fee import Fee
from .models.order import Order
from .models.order import OrderLine
from .models.property import Property


class OrderLineInline(admin.TabularInline):
    model = OrderLine
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderLineInline]


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    pass
    # exclude = (
    #     "stripe_product_id",
    #     "stripe_price_id",
    # )


@admin.register(Fee)
class FeeAdmin(admin.ModelAdmin):
    pass
    # exclude = (
    #     "stripe_product_id",
    #     "stripe_price_id",
    # )


admin.site.register(Property)
