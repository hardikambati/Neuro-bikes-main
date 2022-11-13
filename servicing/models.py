from django.db import models
import datetime

from accounts.models import UserProfile
from store.models import Bike

# Create your models here.

STATUS = (
    ('PENDING', 'PENDING'),
    ('COMPLETED', 'COMPLETED')
)

class ServiceOrder(models.Model):

    user = models.ForeignKey(
        to=UserProfile, 
        on_delete=models.CASCADE, 
        related_name="customer"
    )
    bike = models.ForeignKey(
        to=Bike, 
        on_delete=models.CASCADE
    )
    technician = models.ForeignKey(
        to=UserProfile, 
        on_delete=models.DO_NOTHING, 
        related_name="technician",
        blank=True,
        null=True,
        limit_choices_to={'is_staff': True}
    )
    estimated_date = models.DateField(
        default=datetime.datetime.now() + datetime.timedelta(days=2),
        blank=True,
        null=True,
    
    )
    status = models.CharField(
        max_length=255, 
        choices=STATUS, 
        default="PENDING"
    )

    def __str__(self):

        return self.user.username