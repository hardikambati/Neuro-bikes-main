from django.db import models

from servicing.models import ServiceOrder

# Create your models here.

PAYMENT_MODES = (
    ('ONLINE', 'ONLINE'),
    ('OFFLINE', 'OFFLINE'),
)

PAYMENT_STATUS = (
    ('PENDING', 'PENDING'),
    ('COMPLETED', 'COMPLETED'),
)

class Payment(models.Model):

    amount = models.FloatField(blank=False)
    payment_type = models.CharField(max_length=20, choices=PAYMENT_MODES)
    payment_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, blank=False) 

    def save(self, *args, **kwargs):

        """
            if payment is OFFLINE, it has be confirmed by admin, thus PENDING
            if payment is ONLINE, then COMPLETED
        """

        if (self.payment_type == "OFFLINE"):
            self.status = "PENDING"
        else:
            self.status = "COMPLETED"

        super(Payment, self).save(*args, **kwargs)


# ! refund data should never be deleted !
class Refund(models.Model):

    username = models.CharField(max_length=255, blank=False)
    refund_amount = models.FloatField(blank=False)
    cancelled_order_id = models.IntegerField(blank=False)
    time_of_refund = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return self.username


class ServicePayment(models.Model):

    amount = models.FloatField(blank=False)
    service_order = models.ForeignKey(to=ServiceOrder, on_delete=models.CASCADE, blank=True)
    payment_type = models.CharField(max_length=20, choices=PAYMENT_MODES, blank=False)
    payment_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, blank=False) 

    def save(self, *args, **kwargs):

        """
            if payment is OFFLINE, it has be confirmed by admin, thus PENDING
            if payment is ONLINE, then COMPLETED
        """

        if (self.payment_type == "OFFLINE"):
            self.status = "PENDING"
        else:
            self.status = "COMPLETED"

        super(ServicePayment, self).save(*args, **kwargs)