from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(vendor_product)
admin.site.register(order)
admin.site.register(company_product)
admin.site.register(notification)
admin.site.register(vendor_product_categories)
admin.site.register(raw_material_requirments)
admin.site.register(bid_details)
admin.site.register(company_notification)
