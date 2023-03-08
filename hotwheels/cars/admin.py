from django.contrib import admin
from .models import TYPE,COMPANY,DETAILS,Order,Information,AdditionalAccessories,Taxandother,INSURANCE,Payment,TestDrive
from import_export.admin import ImportExportModelAdmin
from django.http import HttpResponse
import decimal, csv
from django.contrib.auth.models import User
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

class TYPEAdmin(admin.ModelAdmin):
    list_display = ["name"]
admin.site.register(TYPE,TYPEAdmin)

class COMPANYAdmin(admin.ModelAdmin):
    list_display = ["name"]
admin.site.register(COMPANY,COMPANYAdmin)

class DETAILSAdmin(admin.ModelAdmin):
    list_display = ['stock','car_name','car_type','car_company']
admin.site.register(DETAILS,DETAILSAdmin)

def export_books(modeladmin, request, queryset):
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Order.csv"'
    writer = csv.writer(response)
    writer.writerow([
        'customer name','car name','Date_of_booking','Address','LicenceIDNumber','Pincode',
        'ContactNumber','application_code','State','City','Accessorieslist','insurance',
        'total','balance_amount','accssamt','road_tax','regst_amt','insuramt'
    ])
    
    order = queryset.values_list('customerid','carnameid','Date_of_booking','Address','LicenceIDNumber','Pincode',
        'ContactNumber','application_code','State','City','Accessorieslist','insurance',
        'total','balance_amount','accssamt','road_tax','regst_amt','insuramt')
    for Order in order:
        writer.writerow(Order)
    return response
export_books.short_description = 'Export to csv'

def export_order(modeladmin, request, queryset):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Order.pdf"'
    
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer,pagesize=letter, bottomup=0)
    

    
    order = queryset.values_list('customerid','carnameid','Date_of_booking','Address','LicenceIDNumber','Pincode',
        'ContactNumber','application_code','State','City','Accessorieslist','insurance',
        'total','balance_amount','accssamt','road_tax','regst_amt','insuramt')

    

    for Order in order:
        customername = User.objects.get(id=Order[0])
        ascarname = DETAILS.objects.get(id=Order[1])
        tax_id = Order[11][2]
        

        if tax_id:
            taxname = INSURANCE.objects.get(id=int(tax_id))

        access_name = ""
        accessorylist = eval(Order[10])
        for i in accessorylist:
            each_access = int(i)
            access_name += AdditionalAccessories.objects.get(id = each_access).Product + " ,"
        access_name = access_name.rstrip(",")   

    
    # handle the case where tax_id is empty
        pdf.drawString(10,20,"HotWheels")
        pdf.drawString(13, 770, "HOTWHEELS")
        pdf.rect(10, 23, 593, 750, stroke=1)
        pdf.setTitle("HotWheels")
        pdf.setFont('Helvetica', 14)
        pdf.drawString(33, 71, "NAME:")
        pdf.drawString(33, 88, "CAR:")
        pdf.drawString(33, 105, "DATE OF BOOKING:")
        pdf.drawString(33, 122, "ADDRESS:")
        pdf.drawString(33, 139, "LICENCE ID:")
        pdf.drawString(33, 156, "PINCODE:")
        pdf.drawString(33, 173, "PHONE NUMBER:")
        pdf.drawString(33, 190, "APPLICATION CODE:")
        pdf.drawString(33, 207, "STATE")
        pdf.drawString(33, 222, "CITY")
        pdf.drawString(33, 239, "ACCESSORIES")
        pdf.drawString(33, 256, "INSURANCE")
        pdf.drawString(33, 273, "total")
        pdf.drawString(33, 290, "BALANCE AMOUNT:")
        pdf.drawString(33, 307, "ACCESSORIES AMOUNT")
        pdf.drawString(33, 323, "ROAD TAX rs")
        pdf.drawString(33, 340, "REGISTRATION AMOUNT:")
        pdf.drawString(33, 356, "INSURANCE AMOUNT")
        
        pdf.drawString(250, 71, str(customername))
        pdf.drawString(250, 88, str(ascarname))
        pdf.drawString(250, 105, str(Order[2]))
        pdf.drawString(250, 122, str(Order[3]))
        pdf.drawString(250, 139, str(Order[4]))
        pdf.drawString(250, 156, str(Order[5]))
        pdf.drawString(250, 173, str(Order[6]))
        pdf.drawString(250, 190, str(Order[7]))
        pdf.drawString(250, 207, str(Order[8]))
        pdf.drawString(250, 222, str(Order[9]))
        pdf.drawString(250, 239, str(access_name))
        pdf.drawString(250, 256, str(taxname.name))
        pdf.drawString(250, 273, str(Order[12]))
        pdf.drawString(250, 290, str(Order[13]))
        pdf.drawString(250, 307, str(Order[14]))
        pdf.drawString(250, 323, str(Order[15]))
        pdf.drawString(250, 340, str(Order[16]))
        pdf.drawString(250, 356, str(Order[17]))
        pdf.showPage()
        
        
    
    pdf.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response
export_order.short_description = "Export to pdf"

class OrderAdmin(ImportExportModelAdmin):
    list_display = ['customerid','carnameid','Date_of_booking']
    actions = [export_books,export_order]
admin.site.register(Order,OrderAdmin)

class InformationAdmin(admin.ModelAdmin):
    list_display = ['carnameid','companyid','typeid']
admin.site.register(Information,InformationAdmin)

class AdditionalAccessoriesAdmin(admin.ModelAdmin):
    list_display = ['Product','price']
admin.site.register(AdditionalAccessories,AdditionalAccessoriesAdmin)

class TaxandotherAdmin(admin.ModelAdmin):
    list_display = ['carnameid','Road_tax','Reg_amt','booking_amount','delivery_days']
admin.site.register(Taxandother,TaxandotherAdmin)

class INSURANCEAdmin(admin.ModelAdmin):
    list_display = ['name','Insurance_amt']
admin.site.register(INSURANCE,INSURANCEAdmin)

class PaymentAdmin(admin.ModelAdmin):
    list_display = ['name','amount','status']
admin.site.register(Payment,PaymentAdmin)

def export_test(modeladmin, request, queryset):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Test.pdf"'
    
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer,pagesize=letter, bottomup=0)
    

    
    order = queryset.values_list('customerid','carnameid','Date_of_booking','Address','LicenceIDNumber','Pincode',
        'ContactNumber','application_code','State','City')

    

    for Order in order:
        customername = User.objects.get(id=Order[0])
        ascarname = DETAILS.objects.get(id=Order[1])
        
        

        

          

    
    # handle the case where tax_id is empty
        pdf.drawString(10,20,"HotWheels")
        pdf.drawString(13, 770, "HOTWHEELS")
        pdf.rect(10, 23, 593, 750, stroke=1)
        pdf.setTitle("HotWheels")
        pdf.setFont('Helvetica', 14)
        pdf.drawString(33, 71, "NAME:")
        pdf.drawString(33, 88, "CAR:")
        pdf.drawString(33, 105, "DATE OF BOOKING:")
        pdf.drawString(33, 122, "ADDRESS:")
        pdf.drawString(33, 139, "LICENCE ID:")
        pdf.drawString(33, 156, "PINCODE:")
        pdf.drawString(33, 173, "PHONE NUMBER:")
        pdf.drawString(33, 190, "APPLICATION CODE:")
        pdf.drawString(33, 207, "STATE")
        pdf.drawString(33, 222, "CITY")
       
        
        pdf.drawString(250, 71, str(customername))
        pdf.drawString(250, 88, str(ascarname))
        pdf.drawString(250, 105, str(Order[2]))
        pdf.drawString(250, 122, str(Order[3]))
        pdf.drawString(250, 139, str(Order[4]))
        pdf.drawString(250, 156, str(Order[5]))
        pdf.drawString(250, 173, str(Order[6]))
        pdf.drawString(250, 190, str(Order[7]))
        pdf.drawString(250, 207, str(Order[8]))
        pdf.drawString(250, 222, str(Order[9]))
        pdf.showPage()
        
        
    
    pdf.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response
export_order.short_description = "Export to pdf"

class TestDriveAdmin(admin.ModelAdmin):
    list_display = ['customerid','carnameid','Date_of_booking']
    actions = [export_test]
admin.site.register(TestDrive,TestDriveAdmin)


# Register your models here.
