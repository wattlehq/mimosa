from django.contrib import admin

from core.models.certificate import Certificate
from core.models.fee import Fee
from core.models.order import Order
from core.models.order import OrderLine
from core.models.order import OrderSession
from core.models.order import OrderSessionLine
from core.models.property import Property


class OrderLineInline(admin.TabularInline):
    model = OrderLine
    extra = 1
    exclude = (
        "fulfilled_at",
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderLineInline]
    exclude = (
        "fulfilled_at",
    )


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
