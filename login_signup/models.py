from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    company_name = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.user.username


class Vendor(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    company_name = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.user.username


class Employee(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
