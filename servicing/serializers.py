from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from . import models
from store.models import Bike
from payments.models import ServicePayment


class ServiceSerializer(serializers.ModelSerializer):

    class Meta:

        model = models.ServiceOrder
        fields = ('estimated_date', 'status')

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        service_payment_query = ServicePayment.objects.filter(service_order = instance)
        if (service_payment_query):
            service_payment_obj = service_payment_query.first()

            representation['amount'] = service_payment_obj.amount 
            representation['payment_type'] = service_payment_obj.payment_type
            representation['payment_date'] = service_payment_obj.payment_date
            representation['payment_status'] = service_payment_obj.status

            technician = ''
            if (instance.technician == None):
                technician = 'Not assigned yet'
            else:
                technician = instance.technician.username
            
            representation['technician'] = technician 

            return representation      
        else:
            return None


class BookServiceSerializer(serializers.Serializer):

    model_number = serializers.CharField(max_length=255, required=True)
    amount = serializers.FloatField(required=True)
    payment_type = serializers.CharField(max_length=255, required=True)

    def validate(self, data):
        
        user = self.context.get("request").user
        model_number = data.get('model_number')
        
        amount = data.get('amount')

        payment_type = data.get('payment_type')
        payment_type = payment_type.upper()

        # only 2 payment modes should be available
        if (payment_type != "ONLINE" and payment_type != "OFFLINE"):
            msg = ('Payment type should be ONLINE or OFFLINE')
            raise serializers.ValidationError(msg)       

        # amount should NOT be negative
        if (amount < 0):
            msg = ('Input amount should be greated than 0')
            raise serializers.ValidationError(msg)       

        bike_query = Bike.objects.filter(model_number=model_number)

        if bike_query:
            bike_object = bike_query.first()
        else:
            msg = ('Invalid Model Number')
            raise serializers.ValidationError(msg) 

        # check for previous active service
        active_service = models.ServiceOrder.objects.filter(user=user, bike=bike_object, status="PENDING")
        if active_service:
            msg = ('Service for this bike is already active')
            raise serializers.ValidationError(msg)             

        data = {
            "user": user, 
            "bike": bike_object,
            "amount": amount,
            "payment_type": payment_type
        }  

        return data


    def create(self, validated_data):

        serviceorder_object = models.ServiceOrder.objects.create(
            user = validated_data['user'],
            bike = validated_data['bike'],
        )

        # create service payment
        ServicePayment.objects.create(
            amount = validated_data['amount'],
            service_order = serviceorder_object,
            payment_type = validated_data['payment_type']
        )

        return serviceorder_object
            


