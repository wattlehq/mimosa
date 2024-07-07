from django.contrib import admin

from core.models.certificate import Certificate
from core.models.fee import Fee
from core.models.order import Order, OrderLine, OrderSession, OrderSessionLine
from core.models.property import Property


class OrderLineInline(admin.TabularInline):
    model = OrderLine
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderLineInline]


class OrderSessionLineInline(admin.TabularInline):
    model = OrderSessionLine
    extra = 1


@admin.register(OrderSession)
class OrderSessionAdmin(admin.ModelAdmin):
    inlines = [OrderSessionLineInline]


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    exclude = (
        "stripe_product_id",
        "stripe_price_id",
    )


@admin.register(Fee)
class FeeAdmin(admin.ModelAdmin):
    exclude = (
        "stripe_product_id",
        "stripe_price_id",
    )


admin.site.register(Property)
