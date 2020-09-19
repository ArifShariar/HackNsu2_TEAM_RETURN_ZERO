from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Customer, Vendor
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import reverse

# Create your views here.
def login(request):

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        return HttpResponseRedirect(reverse('home_page'))

    return render(request, 'auth/login.html')


def signup(request):

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

        elif user_type.lower() == 'vendor':
            user = User.objects.create(username=email, email=email)
            user.set_password(password)
            user.save()
            vendor = Vendor.objects.create(company_name=company_name, user=user)

        return HttpResponseRedirect(reverse('home_page'))

    return render(request, 'auth/signup.html')
