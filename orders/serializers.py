from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from . import models
from store.models import Bike, Warranty
from payments.models import Payment
from . import producer


class OrderListSerializer(serializers.ModelSerializer):
    
    class Meta:

        model = models.Order
        fields = ()

    def to_representation(self, instance):
        payment_query = Payment.objects.filter(id = instance.payment.id)
        payment_object = payment_query.first()
        representation = super().to_representation(instance)

        bike_query = Bike.objects.filter(model_number = instance.bike.model_number)

        if (bike_query):
            # get warranty
            warranty_query = Warranty.objects.filter(bike = bike_query.first())

            if(warranty_query):
                representation['bought_on'] = warranty_query.first().bought_on 
                representation['warranty_upto'] = warranty_query.first().warranty_upto 

        if (payment_query):
            representation['bike'] = instance.bike.model_number 
            representation['amount'] = payment_object.amount 
            representation['payment_type'] = payment_object.payment_type
            representation['payment_date'] = payment_object.payment_date
            representation['status'] = payment_object.status

            return representation
        
        else:
            return None


class UserTransactionSerializer(serializers.Serializer):

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

        bike_query = Bike.objects.filter(model_number=model_number)

        if bike_query:
            bike_object = bike_query.first()

            # check whether bike is for sale or not
            if (bike_object.is_purchased):
                msg = ('Bike is already purchased')
                raise serializers.ValidationError(msg)       

            # check whether amount is equal to bike price
            if (float(amount) == bike_object.price):
                # create payment
                payment_object = Payment.objects.create(
                    amount = amount,
                    payment_type = payment_type
                )

            else:
                msg = ('Input amount should be equal to bike price')
                raise serializers.ValidationError(msg)                

        else:
            msg = ('Bike with specified model number not found')
            raise serializers.ValidationError(msg)

        data = {
            "user": user,
            "bike": bike_object,
            "payment": payment_object
        }

        return data


    def create(self, validated_data):
        
        bike = validated_data['bike']
        user = validated_data['user']
        payment = validated_data['payment']

        # place order
        order_object = models.Order.objects.create(
            user = user,
            bike = bike,
            payment = payment
        )

        # create warranty
        Warranty.objects.create(
            bike = bike
        )

        # remove bike for sale
        bike.is_purchased = True
        bike.save()

        invoice_data = {
            "full_name": user.first_name + ' ' + user.last_name,
            "user": user.username,
            "bike": bike.model_number,
            "category": bike.category.name,
            "color": bike.color.name,
            "amount": payment.amount,
            "payment_type": payment.payment_type,
            "payment_id": payment.id,
        }

        # push data to RabbitMQ queue
        producer.publish(
            'order_created',
            invoice_data
        )

        return order_object


class OrderCancellationSerializer(serializers.Serializer):

    order_id = serializers.IntegerField(required=True)

    def validate(self, data):

        user = self.context.get("request").user
        order_id = data.get('order_id')

        order_query = models.Order.objects.filter(id=order_id)
        
        if (order_id):
            order_object = order_query.first()
            refund_amount = order_object.payment.amount

            # check wheather ordered user is requesting cancellation
            if (order_object.user != user):
                msg = ('Invalid Request - not your Order')
                raise serializers.ValidationError(msg)                

            # check for previous cancellation request
            previous_cancellation_query = models.CancelledOrder.objects.filter(order = order_object)
            
            if (previous_cancellation_query):
                msg = ('Cancellation has already been requested for this Order')
                raise serializers.ValidationError(msg)

        data = {
            "user": user,
            "order_object": order_object,
            "refund_amount": refund_amount
        }

        return data


    def create(self, validated_data):

        user = validated_data['user']
        order = validated_data['order_object']
        refund_amount = validated_data['refund_amount']

        cancelled_order = models.CancelledOrder.objects.create(
            user = user, 
            order = order,
            refund_amount = refund_amount
        )

        return cancelled_order


class CancelledOrderSerializer(serializers.ModelSerializer):
    
    class Meta:

        model = models.CancelledOrder
        fields = ('refund_amount', 'status', 'created_date')

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        bike_query = Bike.objects.filter(model_number = instance.order.bike.model_number)

        if (bike_query):
            representation['bike'] = instance.order.bike.model_number
            return representation
    
        else:
            return None