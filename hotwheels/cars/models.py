from django.db import models
from django.contrib.auth.models import User
import uuid

class TYPE(models.Model):
    class Meta:
        db_table = 'CAR TYPE'
    
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
