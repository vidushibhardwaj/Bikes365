from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(bike)
class BikeModelAdmin(admin.ModelAdmin):
    list_display = ['id','name','model','fuelcap','mileage','topspeed']

@admin.register(order)
class OrderModelAdmin(admin.ModelAdmin):
    list_display = ['id','bikeid','userid','orderdate','startdaytime','enddaytime']
