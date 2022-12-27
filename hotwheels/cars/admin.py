from django.contrib import admin
from .models import TYPE,COMPANY,DETAILS,Order

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
# Register your models here.
