from django.contrib import admin
from .models import Customer, Vendor, Employee, User

# Register your models here.
admin.site.register(Customer)
admin.site.register(Vendor)
admin.site.register(Employee)
