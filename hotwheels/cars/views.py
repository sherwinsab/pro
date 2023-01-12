# Create your views here.

from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.models import User
from django.contrib import auth
from django.shortcuts import redirect
from django.contrib import messages
from urllib import request
from .models import TYPE,COMPANY,DETAILS,Order,AdditionalAccessories,Taxandother,INSURANCE
from .filters import CarDETAILSFilter
import ast
from datetime import datetime,timedelta




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
        print(CARDETAILS)
        data = {
            "id": CARDETAILS.id,
            "user" : request.user
        }
        return render(request,'product_listing_detail.html',{'CARDETAILS':CARDETAILS,'data':data}) 

    return redirect('signin')
    
def addaccessories(request,pk):
    if 'username' in request.session:
        order_verify = Order.objects.filter(customerid=request.user)
        stock_verify = DETAILS.objects.filter(stock=0,pk=pk)
        print(stock_verify)
        if stock_verify:
            return render(request,'trail2.html')
        elif order_verify:
            return render(request,'trail.html')
        CARDETAILS = DETAILS.objects.get(pk=pk)
        ACCESSORIES =  AdditionalAccessories.objects.all()
        insutype = INSURANCE.objects.all()
        return render(request,'additional_accessories.html',{'ACCESSORIES':ACCESSORIES,'CARDETAILS':CARDETAILS,'insutype':insutype})
    return redirect('signin')

def taxinfo(request,pk):
    if 'username' in request.session:
        if request.method == 'POST':
            options = request.POST.getlist('options')
            optionss = request.POST.getlist('optionss')
            tax = Taxandother.objects.get(carnameid=pk)
            CARDETAILS = DETAILS.objects.get(pk=pk)
            accssamt = 0
            for i in options:
                accssdetail = AdditionalAccessories.objects.get(pk=int(i))
                accssamt += accssdetail.price

            insuramt = 0
            for j in optionss:
                insurdetail = INSURANCE.objects.get(pk=int(j))
                insuramt += insurdetail.Insurance_amt
            
            road_tax = (CARDETAILS.price + accssamt) * tax.Road_tax
            regst_amt = (CARDETAILS.price + accssamt) * tax.Reg_amt
            total = (CARDETAILS.price + accssamt + road_tax + regst_amt + insuramt + tax.booking_amount + tax.delivery_cost)
            
            
            request.session['Assessories_list']=options
            request.session['Insurance']=optionss
            request.session['total']=total
        return render(request,'tax_andother_info.html',{'options':options,'insuramt':insuramt,'optionss':optionss,'tax':tax,'CARDETAILS':CARDETAILS,'accssamt':accssamt,'total':total,'road_tax':road_tax,'regst_amt':regst_amt})
    return redirect('signin')

def booknow(request,pk):
    if 'username' in request.session:
        CARDETAILS = DETAILS.objects.get(pk=pk)
        total = request.session.get('total')
        insurance = request.session.get('Insurance')
        print(total)
        return render(request,'booknow.html',{'CARDETAILS':CARDETAILS,'total':total,'insurance':insurance}) 
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
            Accessorieslist = request.session.get('Assessories_list')
            insurance = request.session.get('Insurance')
            total = request.session.get('total')
            carnameid= DETAILS.objects.get(id=oid)
            
            customer=Order(Address=Address,LicenceIDNumber=LicenceIDNumber,Pincode=Pincode,ContactNumber=ContactNumber,
            State=State,City=City,carnameid=carnameid,Accessorieslist=Accessorieslist,total=total,insurance=insurance)
            customer.customerid = request.user
            customer.save();
            carnameid.stock -= 1
            carnameid.save()

        return redirect('shopping_cart')
    return redirect('signin')

def cancelorder(request, oid):
    if 'username' in request.session:
        customer = Order.objects.get(id=oid)
        car_name_id= DETAILS.objects.get(id=customer.carnameid_id)
        car_name_id.stock += 1
        car_name_id.save()
        customer.delete()
        return redirect('product_listing')
    return redirect('signin')   

def shopping_cart(request):
    if 'username' in request.session:
        
        customer = Order.objects.filter(customerid=request.user)
        if not customer:
            return render(request,'trail3.html')
        else:
            carnameid = customer[0].carnameid
        
        #imagefkref

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

            ass_list = ast.literal_eval(customer[0].Accessorieslist)

            a =''
            for i in list(ass_list):
                
                accssdetail = AdditionalAccessories.objects.get(pk=int(i))
                a +=accssdetail.Product+', '
            a = a[:-2]


            
            return render(request,'shopping_cart.html',{'customer':customer,'carscompanynames':carscompanynames,'cartypenames':cartypenames,'a':a,'priceof':priceof}) 
    return redirect('signin')

def tracking_order(request):
    if 'username' in request.session:
        customer = Order.objects.filter(customerid=request.user)
        carnameid = customer[0].carnameid

        car_company = DETAILS.objects.filter(car_name=carnameid).values('car_company')
        car_company_name = COMPANY.objects.filter(pk=car_company[0].get("car_company")).values('name')
        carscompanynames = car_company_name[0].get("name")

        car_type = DETAILS.objects.filter(car_name=carnameid).values('car_type')
        car_type_name = TYPE.objects.filter(pk=car_type[0].get("car_type")).values('name')
        cartypenames = car_type_name[0].get("name")

        delivery_time = Taxandother.objects.filter(carnameid=carnameid)
        delivery_days = delivery_time[0].delivery_days
        current_date = datetime.now()
        purchase_date = customer[0].Date_of_booking.replace(tzinfo=None)
        nodays = current_date - purchase_date
        estmid_date = purchase_date + timedelta(days=delivery_days)
        nodayss = (nodays.total_seconds())/86400
        value = (nodayss/delivery_days)*100
        if value <=1:
            value = 0
        elif value >1 and value <= 15:
            value=10
        elif value >15 and value <= 25:
            value=25
        elif value > 25 and value <= 50:
            value=50
        elif value > 50 and value <= 75:
            value = 75
        elif value > 75 and value <100:
            value = 85
        else:
            value=100
        return render(request,'tracking_page.html',{'customer':customer,'carscompanynames':carscompanynames,'cartypenames':cartypenames,'value':value,'estmid_date':estmid_date}) 
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

def trail2(request):
    template = loader.get_template('trail2.html')
    return HttpResponse(template.render())

def trail3(request):
    template = loader.get_template('trail3.html')
    return HttpResponse(template.render())

def trail4(request):
    template = loader.get_template('trail4.html')
    return HttpResponse(template.render())

def trail5(request):
    template = loader.get_template('trail5.html')
    return HttpResponse(template.render())

def trail6(request):
    template = loader.get_template('trail6.html')
    return HttpResponse(template.render())