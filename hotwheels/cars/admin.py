from django.contrib import admin
from .models import TYPE,COMPANY,DETAILS,Order,Information,AdditionalAccessories

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
    list_display = ['carnameid','companyid','typeid','delivery_days']
admin.site.register(Information,InformationAdmin)

class AdditionalAccessoriesAdmin(admin.ModelAdmin):
    list_display = ['Product','price']
admin.site.register(AdditionalAccessories,AdditionalAccessoriesAdmin)
# Register your models here.
