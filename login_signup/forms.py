from django import forms
from django.contrib.auth.models import User
from .models import Customer, Vendor, Employee

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('email','password')

class CustomerForm(forms.ModelForm):
    class Meta():
        model = Customer
        fields = ('company_name')

class VendorForm(forms.ModelForm):
    class Meta():
        model = Vendor
        fields = ('company_name')

# class EmployeeForm(forms.ModelForm):
#     class Meta():
#         model = Employee
