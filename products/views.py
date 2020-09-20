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

            return HttpResponseRedirect(reverse('home_page'))
        else:
            categories_raw = vendor_product_categories.objects.all()

            categories = []
            for c in categories_raw:
                categories.append(c.category_name[0].upper()+c.category_name[1:])
            dict = {'categories': categories}

            return render(request, 'products/add_product.html', dict)
    else:
        return HttpResponseRedirect(reverse('home_page'))

def vendor_products(request):
    usertype, user = check_usertype(request)

    if usertype == 'vendor':

        products_raw = vendor_product.objects.filter(vendor_fk=user)
        products = []

        for i in range(len(products_raw)):
            products.append( [products_raw[i].name, products_raw[i].amount, products_raw[i].price] )

        # [ ['Pickup Truck', 5, '5000 per 100km'], ['Covered Van', 2, '10000 per 100km'] ]

        dict = {'products': products}

        return render(request, 'products/vendor_products.html', dict)
    else:
        return HttpResponseRedirect(reverse('home_page'))

def vendor_list(request):
        pass
