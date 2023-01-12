from django.contrib import admin
from .models import TYPE,COMPANY,DETAILS,Order,Information,AdditionalAccessories,Taxandother,INSURANCE

class TYPEAdmin(admin.ModelAdmin):
    list_display = ["name"]
admin.site.register(TYPE,TYPEAdmin)

class COMPANYAdmin(admin.ModelAdmin):
    list_display = ["name"]
admin.site.register(COMPANY,COMPANYAdmin)

class DETAILSAdmin(admin.ModelAdmin):
    list_display = ['stock','car_name','car_type','car_company']
admin.site.register(DETAILS,DETAILSAdmin)

class OrderAdmin(admin.ModelAdmin):
    list_display = ['customerid','carnameid','Date_of_booking']
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
# Register your models here.
