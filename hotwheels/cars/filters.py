from dataclasses import fields
import django_filters

from .models import *

class CarDETAILSFilter(django_filters.FilterSet):
    class Meta:
        model = DETAILS
        fields ={'car_type','car_company','fuel_type','trasmission'} #,'trasmission','car_name',,'engine_cc','car_company','price','fuel_efficiency','seating_capacity'
