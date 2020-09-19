from django.db import models
from login_signup import models as md
# Create your models here.
class vendor_product(models.Model):
    name = models.CharField(max_length=30)
    amount = models.CharField(max_length=30)

    def __str__(self):
        # Built-in attribute of django.contrib.auth.models.User !
        return self.name + " amount: "+ self.amount

class order(models.Model):
    order_time = models.DateField()
    order_amount = models.CharField(max_length=30)
    customer_fk = models.ForeignKey(md.Customer , on_delete=models.DO_NOTHING)

class company_product(models.Model):
    name = models.CharField(max_length=30)
    amount = models.CharField(max_length=30)
    order_fk = models.ForeignKey(order, on_delete=models.CASCADE)
    employee_fk = models.ForeignKey(md.Employee , on_delete=models.DO_NOTHING)

    def __str__(self):
        # Built-in attribute of django.contrib.auth.models.User !
        return self.name + " amount: "+ self.amount


class notification(models.Model):
    noti_msg = models.CharField(max_length=100)
    prediction_msg = models.CharField(max_length=100)
    vendor_fk = models.ForeignKey(md.Vendor , on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.noti_msg



