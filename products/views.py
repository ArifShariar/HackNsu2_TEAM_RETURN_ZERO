from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import *
from login_signup.models import *
from datetime import datetime

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

# Create your views here.
def add_vendor_product(request):

    type, instance = check_usertype(request)

    if type=='vendor':

        if request.method == 'POST':

            product_name = request.POST.get('product_name')
            category = request.POST.get('category').lower()
            price = request.POST.get('price')
            stock = request.POST.get('stock')

            visible = False
            if 'visible' in request.POST:
                visible = True

            category_id = None
            if vendor_product_categories.objects.filter(category_name=category).exists():
                category_id = vendor_product_categories.objects.get(category_name=category)

            vendor_product.objects.create( name=product_name, amount=stock, price=price, category_fk=category_id, vendor_fk=instance, public=visible )

            return HttpResponseRedirect(reverse('home_page'))
        else:
            categories_raw = vendor_product_categories.objects.all()

            categories = []
            for c in categories_raw:
                categories.append(c.category_name[0].upper()+c.category_name[1:])
            dict = {'categories': categories}
            dict['raw_materials'] = True

            return render(request, 'products/add_product.html', dict)
    else:
        return HttpResponseRedirect(reverse('home_page'))

def vendor_products(request):
    usertype, user = check_usertype(request)

    if usertype == 'vendor':

        products_raw = vendor_product.objects.filter(vendor_fk=user)
        products = []

        for i in range(len(products_raw)):
            products.append( [i+1, products_raw[i].name, products_raw[i].amount, products_raw[i].price, products_raw[i].public] )

        dict = {'products': products, 'company_name': user.company_name}
        dict['raw_materials'] = True

        return render(request, 'products/vendor_products.html', dict)
    else:
        return HttpResponseRedirect(reverse('home_page'))

def raw_materials(request):

    usertype, _ = check_usertype(request)

    if usertype.lower() == 'admin' or usertype.lower() == 'employee' or usertype.lower() == 'vendor':

        if request.method == "POST":

            req_id = request.POST.get('req_id')
            form_type = request.POST.get('submit')

            if form_type.lower() == 'make':

                proposal = request.POST.get('proposal')

                vendor = Vendor.objects.filter(user=request.user)[0]
                req = raw_material_requirments.objects.get(id=int(req_id))
                req.bids.add(vendor)

                if bid_details.objects.filter(vendor_fk=vendor, req_fk=req).exists():
                    bid_detail = bid_details.objects.filter(vendor_fk=vendor, req_fk=req)[0]
                    bid_detail.proposal = proposal
                    bid_detail.save()
                else:
                    bid_details.objects.create(vendor_fk=vendor, req_fk=req, proposal=proposal)

                return HttpResponseRedirect(reverse('raw_materials'))

            elif form_type.lower() == 'check':
                return HttpResponseRedirect(reverse('bids_view', args=[req_id]))

        dict = {'raw_materials': True}

        if usertype == 'admin' or usertype == 'employee':
            dict['companyA'] = True
        else:
            dict['companyA'] = False

        pending_requirements = raw_material_requirments.objects.filter(vendor_fk=None)
        past_requirements = raw_material_requirments.objects.exclude(vendor_fk=None)

        dict['pending_requirements'] = pending_requirements
        dict['past_requirements'] = past_requirements

        return render(request, 'products/raw_materials.html', dict)

    else:
        return HttpResponseRedirect(reverse('home_page'))

def bids_view(request, req_id):

    usertype, _ = check_usertype(request)

    if usertype == 'admin' or usertype == 'employee':

        if request.method == "POST":

            vendor_email = request.POST.get('vendor_email')

            user = User.objects.get(email=vendor_email)
            vendor = Vendor.objects.filter(user=user)[0]

            req = raw_material_requirments.objects.get(id=req_id)
            req.vendor_fk = vendor
            req.save()

            proposal = bid_details.objects.get(req_fk=req, vendor_fk=vendor).proposal
            noti_msg = "Requirement : {}\n\nProposal : {}".format(req.description, proposal)

            ntfi = notification.objects.create(type="Bid Success", issue_date=datetime.now(), noti_msg=noti_msg)
            ntfi.vendor_fk.add(vendor)
            ntfi.save()

            return HttpResponseRedirect(reverse('raw_materials'))

        dict = {}
        dict['raw_materials'] = True

        dict['req_des'] = raw_material_requirments.objects.get(id=req_id).description

        bids = []

        req = raw_material_requirments.objects.get(id=req_id)

        bids_raw = req.bids.all()

        for bid in bids_raw:

            vendor = Vendor.objects.get(id=bid.id)

            proposal = bid_details.objects.get(req_fk=req, vendor_fk=vendor).proposal
            bids.append([bid.company_name, proposal, bid.user.email])

        dict['bids'] = bids

        return render(request, 'products/bids.html', dict)
    else:
        return HttpResponseRedirect(reverse('home_page'))

def order_raw_materials(request):

    usertype, _ = check_usertype(request)

    if usertype.lower() == 'admin' or usertype.lower() == 'employee':

        categories_raw = vendor_product_categories.objects.all()

        categories = []
        for c in categories_raw:
            categories.append(c.category_name[0].upper()+c.category_name[1:])
        dict = {'categories': categories}

        dict['raw_materials'] = True

        if request.method == "POST":

            description = request.POST.get('description')
            quantity = request.POST.get('quantity')
            category = request.POST.get('category').lower()
            issue_date = datetime.now()

            category_id = None
            if vendor_product_categories.objects.filter(category_name=category).exists():
                category_id = vendor_product_categories.objects.get(category_name=category)

            raw_material_requirments.objects.create(description=description, quantity=quantity, category_fk=category_id, issue_date=issue_date)

            ntfi = notification.objects.create(type="Relevant Bid", issue_date=datetime.now(), noti_msg=description)
            for vendor in Vendor.objects.all():
                products = vendor_product.objects.filter(vendor_fk=vendor, category_fk=category_id)
                if len(products):
                    ntfi.vendor_fk.add(vendor)
                    ntfi.save()

            return HttpResponseRedirect(reverse('raw_materials'))

        return render(request, 'products/order_raw_materials.html', dict)

    else:
        return HttpResponseRedirect(reverse('home_page'))
