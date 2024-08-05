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
from core.models.tax_rate import TaxRate


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


@admin.register(TaxRate)
class TaxRateAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'percentage', 'is_active', 'created_at', 'updated_at'
    ]
    list_filter = ['is_active']
    search_fields = ['name']
    readonly_fields = ['stripe_tax_rate_id', 'created_at', 'updated_at']

    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing an existing object
            return self.readonly_fields + ['name', 'percentage']
        return self.readonly_fields

    def has_delete_permission(self, request, obj=None):
        return False


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
