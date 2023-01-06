from django.db import models
from django.contrib.auth.models import User
import uuid

class TYPE(models.Model):
    class Meta:
        db_table = 'CAR TYPE'
        verbose_name = "Add Car Type And"
        verbose_name_plural = "Car Type"
    
    id = models.BigAutoField(
        primary_key= True,
    )

    name = models.CharField(
        max_length= 50,
        unique= True,
        verbose_name= "Catogoty Name"
    )
    def __str__(self):
        return self.name

class COMPANY(models.Model):
    class Meta:
        db_table = 'CAR COMPANY'
        verbose_name = "Add Car Company And"
        verbose_name_plural = "Car Company"
    
    id = models.BigAutoField(
        primary_key= True,
    )

    name = models.CharField(
        max_length= 50,
        unique= True,
        verbose_name= "Catogoty Name"
    )
    def __str__(self):
        return self.name

class DETAILS(models.Model):
    class Meta:
        db_table = 'CAR DETAILS'
        verbose_name = "Vechile Information"
        verbose_name_plural = "Vechile Information"

    id = models.BigAutoField(
        primary_key= True,
    )
    car_name = models.CharField(
        max_length=255,
        verbose_name="Car Name"
        )
    car_type = models.ForeignKey(
        TYPE,on_delete=models.CASCADE,
        verbose_name="Car Type"
        )
    car_company = models.ForeignKey(
        COMPANY,on_delete=models.CASCADE,
        verbose_name="Car Company"
        )
    stock = models.IntegerField(
        verbose_name="Stock Avaliable"
        )
    price = models.IntegerField(
        verbose_name="Price Of Car"
        )
    fuel_efficiency = models.CharField(
        max_length=255,
        verbose_name="Mileage In Kilometers"
        )
    fuel_tank_capacity = models.CharField(
        max_length=255,
        verbose_name="Fuel Tank Capacity In Liter"
        )
    front_suspension = models.CharField(
        max_length=255,
        verbose_name="Suspension Type Front"
        )
    rear_suspension = models.CharField(
        max_length=255,
        verbose_name="Suspension Type Rear"
        )
    tyre_size = models.IntegerField(
        verbose_name="Tyre Size"
        )
    front_brake = models.CharField(
        max_length=255,
        verbose_name="Front Brake Type"
        )
    rear_brake = models.CharField(
        max_length=255,
        verbose_name="Rear Brake Type"
        )
    ground_clearance = models.CharField(
        max_length=255,
        verbose_name="Ground Clearance In mm"
        )
    seating_capacity = models.IntegerField(
        verbose_name="Total Seat"
        )
    boot_capacity = models.IntegerField(
        verbose_name="Capacity Of Boot Space In Liter"
        )
    max_torque = models.IntegerField(
        verbose_name="Max Torque"
        )
    tra = models.TextChoices(
        'tra', 'Manual Automatic',
        )
    trasmission = models.CharField(
        default=None,
        choices=tra.choices,
        null=True,blank=True,
        max_length=255,
        verbose_name="Type Of Trasmission"
        )
    cylinders = models.IntegerField(
        verbose_name="Max Number Of Cylinders"
        )
    engine_cc = models.IntegerField(
        verbose_name="Engine CC Of Car"
        )
    image1 = models.ImageField(
        upload_to="image/media/",
        blank=True,
        null=True,
        verbose_name="Exterior Image Of Car"
        )
    image2 = models.ImageField(
        upload_to="image/media/",
        blank=True,
        null=True,
        verbose_name="Interior Image Of Car"
        )
    image3 = models.ImageField(
        upload_to="image/media/",
        blank=True,
        null=True,
        verbose_name="Total Look"
        )
    fuel = models.TextChoices('fuel', 
        'PETROL DIESEL ELETRIC',
    )
    fuel_type = models.CharField(
        default=None,
        choices=fuel.choices,
        null=True,
        blank=True,
        max_length=255,
        verbose_name="What Type Of Energy Using (Fuel TYPE)"
        )
    def __str__(self):
        return self.car_name

class Order(models.Model):
    class Meta:
        db_table = 'CUSTOMER ORDER DETAILS'
        verbose_name = "Customer Orders"
        verbose_name_plural = "Customer Booking"
    
    id = models.BigAutoField(
        primary_key= True,
    )
    Address = models.CharField(default=None,null=True,blank=True,max_length=255,verbose_name="House Address Of Customer")
    LicenceIDNumber = models.CharField(default=None,null=True,blank=True,max_length=255,verbose_name="Licence ID Number Of Customer")
    Pincode = models.IntegerField(verbose_name="Pincode Of Customer")
    ContactNumber = models.CharField(default=None,null=True,blank=True,max_length=255,verbose_name="Contact Number Of Customer")
    application_code = models.UUIDField(default = uuid.uuid4,editable = False,verbose_name="Application Id Of Order")
    State = models.CharField(default=None,null=True,blank=True,max_length=255,verbose_name="State")
    City = models.CharField(default=None,null=True,blank=True,max_length=255,verbose_name="City")
    customerid = models.ForeignKey(User ,default=None,on_delete=models.CASCADE,verbose_name="Customer")
    carnameid = models.ForeignKey(DETAILS,on_delete=models.CASCADE,verbose_name="Car Name")
    Date_of_booking = models.DateTimeField(auto_now_add=True,verbose_name="Date Of Booking")
# Create your models here.

class Information(models.Model):
    class Meta:
        db_table = 'INFORMATION OF CARS'
        verbose_name = "Vechile Description"
        verbose_name_plural = "Vechile Description"
    
    id = models.BigAutoField(
        primary_key= True,
    )
    description = models.CharField(default=None,null=True,blank=True,max_length=1200,verbose_name="Description Of The Vehicle")
    general_information = models.CharField(default=None,null=True,blank=True,max_length=1200,verbose_name="General Information Of The Vehicle")
    vehicle_overview = models.CharField(default=None,null=True,blank=True,max_length=1200,verbose_name="Vehicle overview")
    carnameid = models.ForeignKey(DETAILS,on_delete=models.CASCADE,verbose_name="Car Name")
    companyid = models.ForeignKey(COMPANY,on_delete=models.CASCADE,verbose_name="Car Company")
    typeid = models.ForeignKey(TYPE,on_delete=models.CASCADE,verbose_name="Car Type")

class AdditionalAccessories(models.Model):
    class Meta:
        db_table = 'Additional Accessories'
        verbose_name = "Additional Accessories"
        verbose_name_plural = "Additional Accessories"
    
    id = models.BigAutoField(
        primary_key= True,
    )
    image = models.ImageField(
        upload_to="image/media/",
        blank=True,
        null=True,
        verbose_name="Product Image"
        )
    price = models.IntegerField(
        verbose_name="Price Of Product"
        )
    Product = models.CharField(default=None,null=True,blank=True,max_length=255,verbose_name="Product Name (Pixel Size 62x62)")

class Taxandother(models.Model):
    class Meta:
        db_table = 'TAX AND OTHER'
        verbose_name = "Add Tax And Other Detalis"
        verbose_name_plural = "Tax And Other Info"

    id = models.BigAutoField(
        primary_key= True,
    )
    carnameid = models.ForeignKey(DETAILS,on_delete=models.CASCADE,verbose_name="Car Name")
    companyid = models.ForeignKey(COMPANY,on_delete=models.CASCADE,verbose_name="Car Company")
    typeid = models.ForeignKey(TYPE,on_delete=models.CASCADE,verbose_name="Car Type")
    Road_tax = models.IntegerField(verbose_name="Road tax Amount")
    Insurance = models.IntegerField(verbose_name="Insurance Amount")
    Reg_amt = models.IntegerField(verbose_name="Registration Amount")
    delivery_days = models.IntegerField(verbose_name="Delivery Days Of Car")
    delivery_cost = models.IntegerField(verbose_name="Delivery Cost Of The car")
    booking_amount = models.IntegerField(verbose_name="Booking Amount")
    



