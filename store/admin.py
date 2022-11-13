from django.contrib import admin
from . import models

# Register your models here.

admin.site.register([
    models.Category,
    models.Color,
    models.Warranty,
    models.Bike,
])