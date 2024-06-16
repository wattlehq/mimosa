from django.contrib import admin

from .models.certificate import Certificate
from .models.order import Order
from .models.property import Property

admin.site.register(Certificate)
admin.site.register(Property)
admin.site.register(Order)
