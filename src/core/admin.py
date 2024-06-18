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
    exclude = ('email',)


admin.site.register(Certificate)
admin.site.register(Property)
admin.site.register(Fee)
