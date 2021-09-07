from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
# Create your models here.
class bike(models.Model):
    name = models.CharField(max_length=20)
    model = models.CharField(max_length=20)
    fuelcap = models.IntegerField()
    mileage = models.IntegerField()
    topspeed = models.IntegerField()
    costperday = models.IntegerField(default=100)
    available = models.BooleanField(default=True)
    bikeimg = models.ImageField(null=True,blank=True,upload_to="images/")

    def __str__(self):
        return self.name

class order(models.Model):
    bikeid = models.ForeignKey(bike,on_delete=models.DO_NOTHING)
    userid = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    startdaytime = models.DateTimeField()
    enddaytime = models.DateTimeField()
    orderdate = models.DateTimeField(auto_now_add=True)
