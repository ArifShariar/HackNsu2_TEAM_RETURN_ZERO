from django.shortcuts import render

from login_signup import models as ls
from login_signup.models import *
from products.models import *
from .forms import orderForm
from products import models as p
import datetime

# Create your views here.

def check_usertype(request):
    if request.user.is_authenticated:
        if Customer.objects.filter(user=request.user.id).exists():
            return 'customer', Customer.objects.get(user=request.user.id)
        elif Vendor.objects.filter(user=request.user.id).exists():
            return 'vendor', Vendor.objects.get(user=request.user.id)
        elif Employee.objects.filter(user=request.user.id).exists():
            return 'employee', Employee.objects.get(user=request.user.id)
        elif request.user.username == 'return_zero':
            return 'admin', ' '
        else:
            return ' ', ' '
    else:
        return ' ', ' '

def index(request):
    usertype, _ = check_usertype(request)

    dict = {}
    dict['raw_materials'] = False
    if usertype.lower() == 'vendor' or usertype.lower() == 'admin' or usertype.lower() == 'employee':
        dict['raw_materials'] = True

    return render(request, 'index/index.html', dict)


def products(request):

    dict = {}
    dict['raw_materials'] = False

    usertype, _ = check_usertype(request)
    if usertype.lower() == 'vendor' or usertype.lower() == 'admin' or usertype.lower() == 'employee':
        dict['raw_materials'] = True

    dict['products'] = list(p.company_product.objects.all())

    return render(request, 'products/all_product.html', dict)


def place_order(product_obj, amount, customer_obj):
    time = datetime.date.today()
    order = p.order.objects.create(order_time=time, order_amount=amount, customer_fk=customer_obj, product_fk=product_obj)
    order.save();

def order_view(request , pk):
    if request.method == 'POST':
        amount = request.POST.get('amount')
         #amount= Int(amount)
        prod = p.company_product.objects.get(pk = pk)
        customer = list(ls.Customer.objects.filter(user=request.user))[0]
        place_order(prod , amount , customer)
        print("orderplaced")
        #print(amount)
    dict = {}
    pob = p.company_product.objects.get(pk = pk)
    dict['product_name'] = pob.name
    dict['price'] = pob.price
    dict['stock'] = pob.stock
    dict['form'] = orderForm
    dict['raw_materials'] = False
    usertype,_ = check_usertype(request)

    if usertype.lower() == 'vendor' or usertype.lower()=='admin' or usertype.lower()=='employee':
        dict['raw_materials'] = True
    return render(request, 'order/order.html', dict)


    dict = {}
    pob = p.company_product.objects.get(pk = pk)
    dict['product_name'] = pob.name
    dict['price'] = pob.price
    dict['stock'] = pob.stock
    dict['form'] = orderForm
    dict['raw_materials'] = False
    usertype, _ = check_usertype(request)
    if usertype.lower() == 'vendor' or usertype.lower() == 'admin' or usertype.lower() == 'employee':
        dict['raw_materials'] = True
    return render(request, 'order/order.html' , dict)




def customer_order_history_view(request):
    cust_obj = list(ls.Customer.objects.filter(user=request.user))[0]
    #print(cust_obj)
    orders = list(p.order.objects.filter(customer_fk = cust_obj))
    dict={}
    dict['order_list'] = orders
    dict['customer_name'] = cust_obj
    return render(request, 'order/customer_order_history.html' , dict)


def customers(request):
    dict = {}

    dict['raw_materials'] = False
    usertype, _ = check_usertype(request)
    if usertype.lower() == 'vendor' or usertype.lower() == 'admin' or usertype.lower() == 'employee':
        dict['raw_materials'] = True

    dict['customers'] = list(Customer.objects.all())
    return render(request, 'review/customer_review.html', dict)


def vendors(request):
    vendors = []
    vendors_raw = Vendor.objects.all()
    for v in vendors_raw:
        vendors.append([v.company_name, v.user.email, v.user.id])
    dict = {'vendors':vendors}

    dict['raw_materials'] = False
    usertype, _ = check_usertype(request)
    if usertype.lower() == 'vendor' or usertype.lower() == 'admin' or usertype.lower() == 'employee':
        dict['raw_materials'] = True

    return render(request, 'profile/vendor_list.html', dict)


def contact(request):

    dict = {}

    dict['raw_materials'] = False
    usertype, _ = check_usertype(request)
    if usertype.lower() == 'vendor' or usertype.lower() == 'admin' or usertype.lower() == 'employee':
        dict['raw_materials'] = True

    return render(request, 'others/contact.html', dict)

def vendor_public_profile(request, vendor_user_id):

    user = User.objects.get(id=vendor_user_id)
    vendor = Vendor.objects.get(user=user)

    dict = {}
    dict['email'] = user.email
    dict['company_name'] = vendor.company_name
    dict['type'] = 'vendor'

    usertype, user = check_usertype(request)

    dict['vendor_personal'] = False
    dict['companyA'] = False

    public_products = vendor_product.objects.filter(vendor_fk=vendor, public=True)
    dict['public_products'] = public_products

    if vendor.user.id == request.user.id:
        dict['vendor_personal'] = True
    elif usertype.lower() == 'admin' or usertype.lower() == 'employee':
        dict['companyA'] = True

    dict['raw_materials'] = False
    usertype, _ = check_usertype(request)
    if usertype.lower() == 'vendor' or usertype.lower() == 'admin' or usertype.lower() == 'employee':
        dict['raw_materials'] = True

    return render(request, 'profile/vendor_profile.html', dict)
