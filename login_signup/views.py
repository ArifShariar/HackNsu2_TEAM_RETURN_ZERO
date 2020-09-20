from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Customer, Vendor
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Customer, Vendor, Employee

def check_usertype(request):
    if request.user.is_authenticated:
        if Customer.objects.filter(user=request.user.id).exists():
            return 'customer', Customer.objects.get(user=request.user.id)
        elif Vendor.objects.filter(user=request.user.id).exists():
            return 'vendor', Vendor.objects.get(user=request.user.id)
        else:
            return None, None

# Create your views here.
def login_view(request):

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(username=email, password=password)

        if user:
            login(request,user)

            usertype, user = check_usertype(request)

            if usertype == 'customer':
                dict = {}
                dict['email'] = email # will add company
                dict['type'] = usertype
                return render(request, 'profile/customer_profile.html', dict)
            elif usertype == 'vendor':
                dict = {}
                dict['email'] = email # will add company
                dict['type'] = usertype
                return render(request, 'profile/vendor_profile.html', dict)
        else:
            # Handle Failed Login
            return HttpResponse("Invalid login details supplied.")

    return render(request, 'auth/login.html')


def signup_view(request):
    check_usertype(request)
    if request.method == 'POST':

        user_type = request.POST.get('user_type')
        company_name = request.POST.get('company_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if user_type.lower() == 'customer':
            user = User.objects.create(username=email, email=email)
            user.set_password(password)
            user.save()
            customer = Customer.objects.create(company_name=company_name, user=user)

            user = authenticate(username=email, password=password)
            login(request,user)

            dict = {}
            dict['email'] = email
            dict['company_name'] = company_name
            dict['type'] = user_type

            return render(request, 'profile/customer_profile.html', dict)

        elif user_type.lower() == 'vendor':
            user = User.objects.create(username=email, email=email)
            user.set_password(password)
            user.save()
            vendor = Vendor.objects.create(company_name=company_name, user=user)

            user = authenticate(username=email, password=password)
            login(request,user)

            dict = {}
            dict['email'] = email
            dict['company_name'] = company_name
            dict['type'] = user_type

            return render(request, 'profile/vendor_profile.html', dict)

        return HttpResponseRedirect(reverse('home_page'))

    return render(request, 'auth/signup.html')

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('home_page'))

@login_required
def profile(request):

    usertype, user = check_usertype(request)

    if usertype.lower() == 'customer':

        email = request.user.email
        company_name = user.company_name

        dict = {}
        dict['email'] = email
        dict['company_name'] = company_name
        dict['type'] = usertype

        return render(request, 'profile/customer_profile.html', dict)

    elif usertype.lower() == 'vendor':

        email = request.user.email
        company_name = user.company_name

        dict = {}
        dict['email'] = email
        dict['company_name'] = company_name
        dict['type'] = usertype

        return render(request, 'profile/vendor_profile.html', dict)

    return HttpResponseRedirect(reverse('home_page'))
