from django.contrib import admin
from .models import TYPE,COMPANY,DETAILS

class TYPEAdmin(admin.ModelAdmin):
    list_display = ["name"]
admin.site.register(TYPE,TYPEAdmin)

class COMPANYAdmin(admin.ModelAdmin):
    list_display = ["name"]
admin.site.register(COMPANY,COMPANYAdmin)

class DETAILSAdmin(admin.ModelAdmin):
    list_display = ['stock','car_name','car_type','car_company','price','fuel_efficiency','fuel_tank_capacity','front_suspension','rear_suspension','tyre_size','front_brake','rear_brake','ground_clearance','seating_capacity','boot_capacity','max_torque','trasmission','cylinders','engine_cc','image1','image1','image1']
admin.site.register(DETAILS,DETAILSAdmin)

# Register your models here.
