# Create your views here.

from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.models import User
from django.contrib import auth
from django.shortcuts import redirect
from django.contrib import messages
from urllib import request
from .models import TYPE,COMPANY,DETAILS,Order
from .filters import CarDETAILSFilter



def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render())

def signup(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        
        if password==confirm_password:
            if User.objects.filter(username=username).exists():
                messages.info(request,'Username Taken')
                return redirect('signup')

            elif User.objects.filter(email=email).exists():
                messages.info(request,'Email Taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username,first_name=first_name,last_name=last_name,email=email,password=confirm_password)
                user.save();
                print('user created')
        else:
            messages.info(request,'Password not matching')
            return redirect('signup')
        return redirect('index')
    else:
        return render(request,'signup.html')


def signin(request):
    if 'username' in request.session:
        return redirect('product_listing')
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username,password=password)

        if user is not None:
                request.session['username'] = username
                auth.login(request, user)
                return redirect('product_listing')
        else:
                messages.info(request,'Invalid Credentials')
                return redirect('signin')

    else:
        return render(request,'signin.html')

def logout(request):
    auth.logout(request)
    return redirect('index')

def product_listing(request):
    if 'username' in request.session:
        CARDETAILS = DETAILS.objects.all()
        myFilter = CarDETAILSFilter(request.GET, queryset=CARDETAILS)
        return render(request,'product_listing.html',{'myFilter':myFilter})
    return redirect('signin')

def product_listing_detail(request,pk):
    if 'username' in request.session:
        CARDETAILS = DETAILS.objects.get(pk=pk)
        return render(request,'product_listing_detail.html',{'CARDETAILS':CARDETAILS}) 
    return redirect('signin')

def booknow(request,pk):
    if 'username' in request.session:
        CARDETAILS = DETAILS.objects.get(pk=pk)
        return render(request,'booknow.html',{'CARDETAILS':CARDETAILS}) 
    return redirect('signin')

def add_to_cart(request, oid):
    if 'username' in request.session:
        if request.method =='POST':
            Address = request.POST['Address']
            LicenceIDNumber = request.POST['LicenceIDNumber']
            Pincode = request.POST['Pincode']
            ContactNumber = request.POST['ContactNumber']
            State = request.POST['State']
            City = request.POST['City']
            carnameid= DETAILS.objects.get(id=oid)
            

            customer=Order(Address=Address,LicenceIDNumber=LicenceIDNumber,Pincode=Pincode,ContactNumber=ContactNumber,State=State,City=City,carnameid=carnameid)
            customer.customerid = request.user
            customer.save();
            carnameid.stock -= 1
            carnameid.save()

        return redirect('shopping_cart')
    return redirect('signin')
    

def shopping_cart(request):
    if 'username' in request.session:
        
        customer = Order.objects.filter(customerid=request.user)
        carnameid = customer[0].carnameid

        #carcompanyfkref
        car_company = DETAILS.objects.filter(car_name=carnameid).values('car_company')
        car_company_name = COMPANY.objects.filter(pk=car_company[0].get("car_company")).values('name')
        carscompanynames = car_company_name[0].get("name")

        #cartypefkref
        car_type = DETAILS.objects.filter(car_name=carnameid).values('car_type')
        car_type_name = TYPE.objects.filter(pk=car_type[0].get("car_type")).values('name')
        cartypenames = car_type_name[0].get("name")

        #carprice
        price = DETAILS.objects.filter(car_name=carnameid).values('price')
        priceof = price[0].get("price")
        
        a = 5000+15000+priceof

        
        return render(request,'shopping_cart.html',{'customer':customer,'carscompanynames':carscompanynames,'cartypenames':cartypenames,'priceof':priceof,'a':a}) 
    return redirect('signin')
    
def user_profile(request):
    template = loader.get_template('user_profile.html')
    return HttpResponse(template.render())

def favourite_products(request):
    template = loader.get_template('favourite_products.html')
    return HttpResponse(template.render())

def error404(request):
    template = loader.get_template('404.html')
    return HttpResponse(template.render())
    
def trail(request):
    template = loader.get_template('trail.html')
    return HttpResponse(template.render())