from django.contrib import admin
from .models import vendor_product, order, company_product, notification, vendor_product_categories

# Register your models here.
admin.site.register(vendor_product)
admin.site.register(order)
admin.site.register(company_product)
admin.site.register(notification)
admin.site.register(vendor_product_categories)
