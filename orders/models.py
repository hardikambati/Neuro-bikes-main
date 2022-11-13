from django.db import models

from accounts.models import UserProfile
from store.models import Bike
from payments.models import Payment, Refund

# Create your models here.

class Order(models.Model):

    user = models.ForeignKey(to=UserProfile, on_delete=models.CASCADE)
    bike = models.ForeignKey(to=Bike, on_delete=models.DO_NOTHING)
    payment = models.ForeignKey(to=Payment, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)


REFUND_STATUS = (
    ('PENDING', 'PENDING'),
    ('ACCEPTED', 'ACCEPTED'),
    ('REJECTED', 'REJECTED'),
)

class CancelledOrder(models.Model):

    user = models.ForeignKey(to=UserProfile, on_delete=models.CASCADE)
    order = models.ForeignKey(to=Order, on_delete=models.DO_NOTHING)
    refund_amount = models.FloatField(blank=False) 

    # when ACCEPTED, add data to refund table
    status = models.CharField(max_length=20, choices=REFUND_STATUS, default="PENDING")
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        
        return self.user.username


    def save(self, *args, **kwargs):

        if (self.status == "ACCEPTED"):

            # create refund
            Refund.objects.create(
                username = self.user.username,
                refund_amount = self.refund_amount,
                cancelled_order_id = self.id
            )

        super(CancelledOrder, self).save(*args, **kwargs)