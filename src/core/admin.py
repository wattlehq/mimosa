from django.contrib import admin

from core.forms.settings import SettingsForm
from core.models.certificate import Certificate
from core.models.fee import Fee
from core.models.order import Order
from core.models.order import OrderLine
from core.models.order import OrderSession
from core.models.order import OrderSessionLine
from core.models.property import Property
from core.models.settings import Settings
from core.models.certificate_bundle import CertificateBundle


class OrderLineInline(admin.TabularInline):
    model = OrderLine
    extra = 1
    exclude = ("fulfilled_at",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderLineInline]
    exclude = ("fulfilled_at",)
    readonly_fields = ("order_hash",)


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


@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
    form = SettingsForm

    def has_add_permission(self, request):
        # Prevent adding new settings if one already exists.
        return not Settings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        # Prevent deletion of settings.
        return False


admin.site.register(Property)

@admin.register(CertificateBundle)
class CertificateBundleAdmin(admin.ModelAdmin):
    list_display = ('parent_certificate', 'child_certificate')
