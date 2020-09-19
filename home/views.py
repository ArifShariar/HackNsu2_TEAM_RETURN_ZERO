from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'index/index.html')

def products(request):
    return render(request, 'products/all_product.html')
