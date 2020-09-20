from django.db import models
from login_signup import models as md

# Create your models here.
class vendor_product_categories(models.Model):
    category_name = models.CharField(max_length=50, null=False, unique=True)

    def __str__(self):
        return self.category_name

class vendor_product(models.Model):
    name = models.CharField(max_length=30)
    amount = models.IntegerField()
    price = models.FloatField(null=True)
    category_fk = models.ForeignKey(vendor_product_categories, on_delete=models.DO_NOTHING, null=True)
    vendor_fk = models.ForeignKey(md.Vendor, on_delete=models.CASCADE, null=True)

    def __str__(self):
        # Built-in attribute of django.contrib.auth.models.User !
        return self.name + " amount: "+ self.amount

class company_product(models.Model):
    name = models.CharField(max_length=30)
    amount = models.CharField(max_length=30)
    stock = models.IntegerField(null=True)

    def __str__(self):
        # Built-in attribute of django.contrib.auth.models.User !
        return self.name + " amount: "+ self.amount

class order(models.Model):
    order_time = models.DateField()
    order_amount = models.IntegerField()
    customer_fk = models.ForeignKey(md.Customer , on_delete=models.DO_NOTHING, null=True)
    product_fk = models.ForeignKey(company_product, on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        # Built-in attribute of django.contrib.auth.models.User !
        return self.ordered_product + " amount: "+ self.order_amount

class notification(models.Model):
    noti_msg = models.CharField(max_length=100)
    prediction_msg = models.CharField(max_length=100)
    vendor_fk = models.ForeignKey(md.Vendor , on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        return self.noti_msg
