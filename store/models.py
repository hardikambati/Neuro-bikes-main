from django.db import models
import datetime

# Create your models here.

class Category(models.Model):

    name = models.CharField(max_length=255, blank=False)

    def __str__(self):
        return self.name


class Color(models.Model):

    name = models.CharField(max_length=255, blank=False)

    def __str__(self):
        return self.name


class Bike(models.Model):

    model_number = models.CharField(max_length=555, blank=False, unique=True)
    category = models.ForeignKey(to=Category, on_delete=models.DO_NOTHING)
    color = models.ForeignKey(to=Color, on_delete=models.DO_NOTHING, blank=False)
    price = models.FloatField(blank=False)
    is_purchased = models.BooleanField(default=False)

    def __str__(self):
        return self.model_number


class Warranty(models.Model):

    bike = models.ForeignKey(to=Bike, on_delete=models.CASCADE)
    bought_on = models.DateField(auto_now_add=True)
    warranty_upto = models.DateField(default=datetime.datetime.now() + datetime.timedelta(days=100))

    def __str__(self):
        return self.bike.model_number