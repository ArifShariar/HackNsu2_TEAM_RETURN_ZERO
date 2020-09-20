from django.shortcuts import render

from products import models as p
# Create your views here.

def index(request):
    return render(request, 'index/index.html')


def products(request):
    dict = {}
    dict['products'] = list(p.company_product.objects.all())
    print(list(p.company_product.objects.all()))
    return render(request, 'products/all_product.html',dict)


def customers(request):
    return render(request, 'review/customer_review.html')


def vendors(request):
    return render(request, 'review/vendor_review.html')


def contact(request):
    return render(request, 'others/contact.html')
