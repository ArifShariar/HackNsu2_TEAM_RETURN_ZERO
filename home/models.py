from django.db import models

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

class company_product(models.Model):
    name = models.CharField(max_length=30)
    amount = models.CharField(max_length=30)
    order_fk = models.ForeignKey(order, on_delete=models.CASCADE)

    def __str__(self):
        # Built-in attribute of django.contrib.auth.models.User !
        return self.name + " amount: "+ self.amount

class notification(models.Model):
    noti_msg = models.CharField(max_length=100)
    prediction_msg = models.CharField(max_length=100)

    def __str__(self):
        return self.noti_msg


