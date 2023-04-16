# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.contrib.auth.models import User
from django.contrib import auth
from django.shortcuts import redirect
from django.contrib import messages
from .models import TYPE,COMPANY,DETAILS,Order,AdditionalAccessories,Taxandother,INSURANCE,Payment,TestDrive,FeaturedVechiles
from .filters import CarDETAILSFilter
import ast
from datetime import datetime,timedelta
from twilio.rest import Client
import razorpay
import json
from .constants import PaymentStatus
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse




from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from django.db.models import Sum
import openai
import requests

import cv2
from pytesseract import pytesseract
from django.http import StreamingHttpResponse

openai.api_key = "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" # Replace with your actual API key
model_engine = "text-davinci-003"
# import numpy as np
# import pandas as pd

from .recommend import rec_obj


def index(request):
    featured_vechiles = FeaturedVechiles.objects.all()
    context = {'featured_vechiles': featured_vechiles}
    return render(request, 'index.html', context)
    

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
        #code for recommendtion
        recommendcardetalis = []
        orderDETAILS = Order.objects.filter(carnameid=pk)
        if orderDETAILS:
            result = rec_obj.process_recom(pk)
           
            for i in result:
                data = DETAILS.objects.get(pk=i)
                recommendcardetalis.append({
                        "carname": data.car_name,
                        "image": data.image3,
                        "price": data.price,
                        "id":data.id,
                        "average_rating":round(data.average_rating,2)
                        # Add more fields here as needed
                    })     
        
        #code for selected car detalis    
        CARDETAILS = DETAILS.objects.get(pk=pk)
        data = {
            "id": CARDETAILS.id,
            "user" : request.user
        }
        return render(request,'product_listing_detail.html',{'CARDETAILS':CARDETAILS,'data':data,'recommendcardetalis':recommendcardetalis}) 

    return redirect('signin')

# def search(requset):
#     if requset.method == "POST"
#         searched = requset.POST['searched']
#         CARDETAILS = DETAILS.objects.all()
#         return render(request,'product_listing.html',{'searched':searched})
#     else:
#         pass


def testdrive_booking(request,pk):
    if 'username' in request.session:
        #code for selected car detalis    
        CARDETAILS = DETAILS.objects.get(pk=pk)
        data = {
            "id": CARDETAILS.id,
            "user" : request.user
        }
        return render(request,'testdrive_booking.html',{'CARDETAILS':CARDETAILS,'data':data})
    return redirect('signin')

def testdrive_booked(request, oid):
    if 'username' in request.session:
        if request.method =='POST':
            Address = request.POST['Address']
            LicenceIDNumber = request.POST['LicenceIDNumber']
            Pincode = request.POST['Pincode']
            ContactNumber = request.POST['ContactNumber']
            State = request.POST['State']
            City = request.POST['City']
            dattte = request.POST['birthday']
            
            carnameid= DETAILS.objects.get(id=oid)
            
            customer=TestDrive(Address=Address,LicenceIDNumber=LicenceIDNumber,Pincode=Pincode,ContactNumber=ContactNumber,
            State=State,City=City,carnameid=carnameid,dattte=dattte)
            customer.customerid = request.user
            customer.save();


        return redirect('testdrivecart')
    return redirect('signin')

def testdrivecart(request):
    if 'username' in request.session:
        
        customer = TestDrive.objects.filter(customerid=request.user)
        if not customer:
            return render(request,'trail4.html')
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
            
            return render(request,'test_drive_cart.html',{'customer':customer,'carscompanynames':carscompanynames,'cartypenames':cartypenames,'priceof':priceof}) 
    return redirect('signin')

def testdrive_pdf(request):
    #create bytestream buffer
    buf = io.BytesIO()
    #create canvas
    c = canvas.Canvas(buf,pagesize=letter, bottomup=0)
    c.drawString(10,20,"HotWheels")
    c.drawString(13, 770, "HOTWHEELS")
    c.rect(10, 23, 593, 750, stroke=1)
    #create text obj
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica",14)
    
    #add lines text
    # lines = [
    #         "This is Line 1",
    #         "This is Line 2",
    #         "This is Line 3",
    # ]
    customer = TestDrive.objects.filter(customerid=request.user)
    carnameid = customer[0].carnameid

    car_company = DETAILS.objects.filter(car_name=carnameid).values('car_company')
    car_company_name = COMPANY.objects.filter(pk=car_company[0].get("car_company")).values('name')
    carscompanynames = car_company_name[0].get("name")

#cartypefkref
    car_type = DETAILS.objects.filter(car_name=carnameid).values('car_type')
    car_type_name = TYPE.objects.filter(pk=car_type[0].get("car_type")).values('name')
    cartypenames = car_type_name[0].get("name")

#carprice
    # price = DETAILS.objects.filter(car_name=carnameid).values('price')
    # priceof = price[0].get("price")
    
    name = customer[0].customerid
    auth_cust = User.objects.filter(username=name)
    names = auth_cust[0].first_name + ' ' + auth_cust[0].last_name
    email = auth_cust[0].email
    lines =[]
    
    for order in customer:

        c.drawString(13, 770, "HOTWHEELS")
        c.rect(10, 23, 593, 750, stroke=1)
        c.setTitle("HotWheels")
        c.setFont('Helvetica', 14)
        c.drawString(33, 71, "NAME:")
        c.drawString(33, 88, "CAR:")
        c.drawString(33, 105, "DATE OF BOOKING:")
        c.drawString(33, 122, "ADDRESS:")
        c.drawString(33, 139, "LICENCE ID:")
        c.drawString(33, 156, "PINCODE:")
        c.drawString(33, 173, "PHONE NUMBER:")
        c.drawString(33, 190, "APPLICATION CODE:")
        c.drawString(33, 207, "STATE")
        c.drawString(33, 222, "CITY")
        c.drawString(33,238,"COMPANY:")
        c.drawString(33,254,"TYPE:")
        c.drawString(33,270,"EMAIL:")
       
        
        c.drawString(250, 71,"" +  names)
        c.drawString(250, 88,"" + str(order.carnameid))
        c.drawString(250, 105,"" +  carscompanynames)
        c.drawString(250, 122,"" +  cartypenames)
        c.drawString(250, 139,"" +  str(order.Date_of_booking))
        c.drawString(250, 156,"" +  email)
        c.drawString(250, 173,"" +  str(order.Address))
        c.drawString(250, 190,"" +  str(order.LicenceIDNumber))
        c.drawString(250, 207,"" +  str(order.Pincode))
        c.drawString(250, 222,""+ str(order.ContactNumber))
        c.drawString(250,238,"" +  carscompanynames)
        c.drawString(250,254,"" +  cartypenames)
        c.drawString(250,270,"" +  email)
        c.showPage()
        
    #loop
    for line in lines:
        textob.textLine(line)

    c.drawText(textob)
    
    c.save()
    buf.seek(0)

    return FileResponse(buf, as_attachment=True, filename='TestBooking.pdf')

def testdrivecancel(request, oid):
    if 'username' in request.session:
        customer = TestDrive.objects.get(id=oid)
        customer.delete()
        return redirect('product_listing')
    return redirect('signin')

@login_required(login_url='signin')
def testdriverating(request):
    if request.method == 'POST':
        testdict = {}
        testdict = json.dumps(request.POST)
        dict_obj = json.loads(testdict)

        # Remove the "csrfmiddlewaretoken" key if it exists
        if "csrfmiddlewaretoken" in dict_obj:
            del dict_obj["csrfmiddlewaretoken"]

        # Print the resulting dictionary
        
        for key, value in dict_obj.items():
            testdrive_id = key
            rating = value
        
        # Get the TestDrive object for the given order_id
        test_drive = TestDrive.objects.get(id=testdrive_id)

        # Update the TestDrive rating with the selected rating
        test_drive.Test_drive_rating = rating
        test_drive.save()

        # Redirect to the test drive cart page
        return redirect('testdrivecart')

    # If the request method is not POST, redirect to the test drive cart page
    return redirect('testdrivecart')


def addaccessories(request,pk):
    if 'username' in request.session:
        order_verify = Order.objects.filter(customerid=request.user)
        stock_verify = DETAILS.objects.filter(stock=0,pk=pk)
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
            
            request.session['road_tax']=road_tax
            request.session['regst_amt']=regst_amt
            request.session['insuramt']=insuramt
            request.session['accssamt']=accssamt
            
            request.session['Assessories_list']=options
            request.session['Insurance']=optionss
            request.session['total']=total
        return render(request,'tax_andother_info.html',{'options':options,'insuramt':insuramt,'optionss':optionss,
        'tax':tax,'CARDETAILS':CARDETAILS,'accssamt':accssamt,'total':total,'road_tax':road_tax,'regst_amt':regst_amt})
    return redirect('signin')

def booknow(request,pk):
    if 'username' in request.session:
        CARDETAILS = DETAILS.objects.get(pk=pk)
        data = {
            "id": CARDETAILS.id,
            "user" : request.user
        }
        total = request.session.get('total')
        insurance = request.session.get('Insurance')
        
        return render(request,'booknow.html',{'CARDETAILS':CARDETAILS,'total':total,'insurance':insurance,'data':data}) 
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
            accssamt = request.session.get('accssamt')
            road_tax = request.session.get('road_tax')
            regst_amt = request.session.get('regst_amt')
            insuramt = request.session.get('insuramt')
            

            carnameid= DETAILS.objects.get(id=oid)
            
            customer=Order(Address=Address,LicenceIDNumber=LicenceIDNumber,Pincode=Pincode,ContactNumber=ContactNumber,
            accssamt=accssamt,road_tax=road_tax,regst_amt=regst_amt,insuramt=insuramt,
            State=State,City=City,carnameid=carnameid,Accessorieslist=Accessorieslist,total=total,insurance=insurance,balance_amount=total)
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

def shopping_cart_pdf(request):
    #create bytestream buffer
    buf = io.BytesIO()
    #create canvas
    c = canvas.Canvas(buf,pagesize=letter, bottomup=0)
    c.drawString(10,20,"HotWheels")
    c.drawString(13, 770, "HOTWHEELS")
    c.rect(10, 23, 593, 750, stroke=1)
    #create text obj
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica",14)
    
    #add lines text
    # lines = [
    #         "This is Line 1",
    #         "This is Line 2",
    #         "This is Line 3",
    # ]
    customer = Order.objects.filter(customerid=request.user)
    carnameid = customer[0].carnameid

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

    name = customer[0].customerid
    auth_cust = User.objects.filter(username=name)
    names = auth_cust[0].first_name + ' ' + auth_cust[0].last_name
    email = auth_cust[0].email

    ins_list = ast.literal_eval(customer[0].insurance)

    b =''
    for j in list(ins_list):
        insdetails = INSURANCE.objects.get(pk=int(j))
        b +=insdetails.name+', '
    b = b[:-2]

    lines =[]
    
    for order in customer:
        
        c.drawString(33, 71, "NAME:",lines.append("                               " +  names))
        c.drawString(33, 88, "CAR:", lines.append("                               " + str(order.carnameid))),
        c.drawString(33, 105, "COMPANY:",lines.append("                               " +  carscompanynames)),
        c.drawString(33, 122, "TYPE:",lines.append("                               " +  cartypenames)),
        c.drawString(33, 139, "ON ROAD PRICE:",lines.append("                               " +  str(order.total))),
        c.drawString(33, 156, "DATE OF BOOKING:",lines.append("                               " +  str(order.Date_of_booking))),
        c.drawString(33, 173, "EMAIL:",lines.append("                               " +  email)),
        c.drawString(33, 190, "ADDRESS:",lines.append("                               " +  str(order.Address))),
        c.drawString(33, 207, "LICENCE ID:",lines.append(str("                               " +  order.LicenceIDNumber))),
        c.drawString(33, 222, "PINCODE:",lines.append("                               " +  str(order.Pincode))),
        c.drawString(33, 239, "PHONE NUMBER:",lines.append("                               " +  str(order.ContactNumber))),
        c.drawString(33, 256, "APPLICATION CODE:",lines.append("                               " +  str(order.application_code))),
        c.drawString(33, 273, "STATE:",lines.append(str("                               " +  order.State))),
        c.drawString(33, 290, "CITY:",lines.append(str("                               " +  order.City))),
        c.drawString(33, 307, "ACCESSORIES:",lines.append("                               " +  a)),
        c.drawString(33, 323, "INSURANCE:",lines.append("                               " +  b)),
        c.drawString(33, 340, "BALANCE AMOUNT:",lines.append("                               " +  str(order.balance_amount))),
        c.drawString(33, 356, "ROAD TAX rs:",lines.append("                               " +  str(order.road_tax))),
        c.drawString(33, 374, "REGISTRATION AMOUNT:",lines.append("                               " +  str(order.regst_amt))),
        c.drawString(33, 391, "INSURANCE AMOUNT:",lines.append("                               " +  str(order.insuramt))),
        c.drawString(33, 408, "ACCESSORIES AMOUNT:",lines.append("                               " +  str(order.accssamt))),
        lines.append("")
    #loop
    for line in lines:
        textob.textLine(line)

    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)

    return FileResponse(buf, as_attachment=True, filename='Booking.pdf')

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
            
            account_sid = 'ACbd373e62581246849c1d7d98f3f1f560'
            auth_token = '5ce15071bacc9cc0909ea8fc8813a44b'
            client = Client(account_sid, auth_token)

            message = client.messages.create(
                                                body=f"HotWheels, Your New Car {carnameid} Has Arrived At The Showroom Delivery Will Be in 5 Days",
                                                from_='+14109364038',
                                                to='+917560893894'
                                            )

            
          
        else:
            value=100
        return render(request,'tracking_page.html',{'customer':customer,'carscompanynames':carscompanynames,'cartypenames':cartypenames,'value':value,'estmid_date':estmid_date}) 
    return redirect('signin') 

def checkout(request):
    if 'username' in request.session:
        customer = Order.objects.filter(customerid=request.user)
        carnameid = customer[0].carnameid

        car_company = DETAILS.objects.filter(car_name=carnameid).values('car_company')
        car_company_name = COMPANY.objects.filter(pk=car_company[0].get("car_company")).values('name')
        carscompanynames = car_company_name[0].get("name")
        

        car_type = DETAILS.objects.filter(car_name=carnameid).values('car_type')
        car_type_name = TYPE.objects.filter(pk=car_type[0].get("car_type")).values('name')
        cartypenames = car_type_name[0].get("name")


        price = int(customer[0].total)*100

        
        return render(request,'checkout.html',{'price':price,'customer':customer,'carscompanynames':carscompanynames,'cartypenames':cartypenames})
    return redirect('signin')

def order_payment(request):
    if 'username' in request.session:
        if request.method == "POST":
            customer = Order.objects.filter(customerid=request.user)
            carnameid = customer[0].carnameid

            car_company = DETAILS.objects.filter(car_name=carnameid).values('car_company')
            car_company_name = COMPANY.objects.filter(pk=car_company[0].get("car_company")).values('name')
            carscompanynames = car_company_name[0].get("name")
        

            car_type = DETAILS.objects.filter(car_name=carnameid).values('car_type')
            car_type_name = TYPE.objects.filter(pk=car_type[0].get("car_type")).values('name')
            cartypenames = car_type_name[0].get("name")

            contactnumber = customer[0].ContactNumber

            price = int(customer[0].total)
            
            
            
            name = customer[0].customerid
            auth_cust = User.objects.filter(username=name)
            names = auth_cust[0].first_name + ' ' + auth_cust[0].last_name
            email = auth_cust[0].email
            amount = price/2
            amount1 = 25000
            amount2 = 25000
           
            client = razorpay.Client(auth=("rzp_test_1sFSQT1jdm1swd", "PYkvqUl4Zx2EfNeRAAf9FXJs"))
            razorpay_order = client.order.create(
            {"amount": amount1*100, "currency": "INR", "payment_capture": "1"}
            )
            
            order = Payment.objects.create( 
            name=names, amount=amount2, provider_order_id=razorpay_order["id"]
            )
            order.save()

            return render(request,'payment.html',{'email':email,'contactnumber':contactnumber,'customer':customer,'carscompanynames':carscompanynames,'cartypenames':cartypenames,
            "callback_url": "http://" + "127.0.0.1:8000" + "/cars/callback/",
            "razorpay_key": "rzp_test_1sFSQT1jdm1swd",
            "order": order,
            }
            )
        return render(request, "payment.html")
#from here edit
@csrf_exempt
def callback(request):
    def verify_signature(response_data):
        client = razorpay.Client(auth=("rzp_test_1sFSQT1jdm1swd", "PYkvqUl4Zx2EfNeRAAf9FXJs"))
        return client.utility.verify_payment_signature(response_data)
    if "razorpay_signature" in request.POST:
        
        payment_id = request.POST.get("razorpay_payment_id", "")
        provider_order_id = request.POST.get("razorpay_order_id", "")
        signature_id = request.POST.get("razorpay_signature", "")
        order = Payment.objects.get(provider_order_id=provider_order_id)
        order.payment_id = payment_id
        order.signature_id = signature_id
        order.save()
        
        

        if verify_signature(request.POST):
            order.status = PaymentStatus.SUCCESS
            order.save()
            #reduce 25000 advance from total  amount
            customer_name = order.name
            split_name = customer_name.split()
            first_name = split_name[0]
            last_name = split_name[-1]
            
            customer_id = User.objects.filter(first_name = first_name, last_name=last_name)
            cus_id = customer_id[0].id
            
            customer = Order.objects.get(customerid=cus_id)

            balance = customer.balance_amount - 25000
            customer.balance_amount = balance
            customer.save()
            return render(request, "callback.html", context={"status": order.status})
        else:
            order.status = PaymentStatus.FAILURE
            order.save()
            return render(request, "callback.html", context={"status": order.status})
    else:
        payment_id = json.loads(request.POST.get("error[metadata]")).get("payment_id")
        provider_order_id = json.loads(request.POST.get("error[metadata]")).get(
        "order_id"
        )
        order = Payment.objects.get(provider_order_id=provider_order_id)
        order.payment_id = payment_id
        order.status = PaymentStatus.FAILURE
        order.save()
        return render(request, "callback.html", context={"status": order.status})
    

def userprofile(request):
    if 'username' in request.session:
        # customer = Order.objects.filter(customerid=request.user)
        # carnameid = customer[0].carnameid

        # car_company = DETAILS.objects.filter(car_name=carnameid).values('car_company')
        # car_company_name = COMPANY.objects.filter(pk=car_company[0].get("car_company")).values('name')
        # carscompanynames = car_company_name[0].get("name")
    

        # car_type = DETAILS.objects.filter(car_name=carnameid).values('car_type')
        # car_type_name = TYPE.objects.filter(pk=car_type[0].get("car_type")).values('name')
        # cartypenames = car_type_name[0].get("name")

        # contactnumber = customer[0].ContactNumber
        # price = int(customer[0].total)

        return render(request,'user_profile.html')#'contactnumber':contactnumber,'price':price,'customer':customer,'carscompanynames':carscompanynames,'cartypenames':cartypenames
    return redirect('signin')

def updaterecord(request):
 if 'username' in request.session:
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        id = request.POST['id']
        # about = request.POST['about']
        # skills = request.POST['skills']
        # image = request.FILES.get('avatar')
    #   password = request.POST['password']
        user = User.objects.get(id=id)
        user.first_name = first_name
        user.last_name = last_name

        # user.about = about
        # user.skills = skills 
        # user.image = image
    #   user.password = password
        user.save()
        return redirect('userprofile')

def rating(request):
    if 'username' in request.session:
        customer = Order.objects.get(customerid=request.user)

        rate = int(request.POST.get('rating'))
        customer.rating = rate
        sum_of_ratings = 0
        car_filter = Order.objects.filter(carnameid=customer.carnameid)
        
        car_filter_count = car_filter.count() + 1
        if car_filter.exists():
            sum_of_ratings = car_filter.aggregate(sum_of_ratings=Sum('rating'))['sum_of_ratings']
        else:
            sum_of_ratings = 0 
        sum_of_ratings += rate

        average_rating = sum_of_ratings/car_filter_count
        
        customer.average_rating = average_rating
        customer.save()
        car_detail = DETAILS.objects.get(id=customer.carnameid.id)
        car_detail.average_rating = average_rating
        car_detail.save()
        car_filter.update(average_rating = average_rating)

        return redirect('shopping_cart')
    return redirect('signin')

def favourite_products(request):
    template = loader.get_template('favourite_products.html')
    return HttpResponse(template.render())

def error404(request):
    template = loader.get_template('404.html')
    return HttpResponse(template.render())
    
def trail(request):
    if 'username' in request.session:
        return render(request,'trail.html')
    return redirect('signin')

def trail2(request):
    if 'username' in request.session:
        return render(request,'trail2.html')
    return redirect('signin')
    
def trail3(request):
    if 'username' in request.session:
        return render(request,'trail3.html')
    return redirect('signin')
    
def trail4(request):
    template = loader.get_template('trail4.html')
    return HttpResponse(template.render())

def trail5(request):
    template = loader.get_template('trail5.html')
    return HttpResponse(template.render())


def generate_completion(request):
    if 'username' in request.session:
        prompt = request.POST.get('prompt', '')
        response = openai.Completion.create(
            engine=model_engine,
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5
        )
        completion_text = response.choices[0].text
        context = {
            'completion_text': completion_text
        }
        return render(request, 'trail6.html', context)
    return redirect('signin')

def run(request):
    if 'username' in request.session:
        pass
        return render(request, 'numberPlates.html')
    return redirect('signin')


def numberPlates(request):
    def generate():
        frameWidth = 640    #Frame Width
        franeHeight = 480   # Frame Height
        plateCascade = cv2.CascadeClassifier("E:\PyCharm\hi\haarcascade_russian_plate_number.xml")
        minArea = 500
        cap = cv2.VideoCapture(0)
        cap.set(3,frameWidth)
        cap.set(4,franeHeight)
        cap.set(10,150)
        pytesseract.tesseract_cmd = r'E:/PyCharm/hi/tesseract.exe'
        while True:
            success , img  = cap.read()
            imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            numberPlates = plateCascade .detectMultiScale(imgGray, 1.1, 4)
            for (x, y, w, h) in numberPlates:
                area = w*h
                if area > minArea:
                    imgRoi = img[y:y+h,x:x+w]
                    text = pytesseract.image_to_string(imgRoi)
                    yield f"Number Plate Detected: {text}\n\n"      
    response = StreamingHttpResponse(generate(), content_type='text/event-stream')
    response['Cache-Control'] = 'no-cache'
    return response
    
    
def featured_vechiles(request):
    featured_vechiles = FeaturedVechiles.objects.all()
    context = {'featured_vechiles': featured_vechiles}
    return render(request, 'featured_vechiles.html', context)

def get_news(request):
    if 'username' in request.session:
        url = 'https://newsapi.org/v2/top-headlines?country=us&apiKey=e92090481bc24996a2a89b1f90299cdf'
        response = requests.get(url)
        articles = response.json()['articles']
        return render(request, 'news.html', 
                    {
                        "page": "Newsplatform",
                        "articles": articles
                    })
    return redirect('signin')