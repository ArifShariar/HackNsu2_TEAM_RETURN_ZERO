from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import *
from login_signup.models import *

def check_usertype(request):
    if request.user.is_authenticated:
        if Customer.objects.filter(user=request.user.id).exists():
            return 'customer', Customer.objects.get(user=request.user.id)
        elif Vendor.objects.filter(user=request.user.id).exists():
            return 'vendor', Vendor.objects.get(user=request.user.id)
        else:
            return ' ', ' '

# Create your views here.
def add_vendor_product(request):

    type, instance = check_usertype(request)

    if (type=='vendor'):

        if request.method == 'POST':

            product_name = request.POST.get('product_name')
            category = request.POST.get('category').lower()
            price = request.POST.get('price')
            stock = request.POST.get('stock')

            category_id = None
            if vendor_product_categories.objects.filter(category_name=category).exists():
                category_id = vendor_product_categories.objects.get(category_name=category)

            vendor_product.objects.create( name=product_name, amount=stock, price=price, category_fk=category_id, vendor_fk=instance )

        else:
            return HttpResponseRedirect(reverse('home_page'))
    else:
        return HttpResponseRedirect(reverse('home_page'))
