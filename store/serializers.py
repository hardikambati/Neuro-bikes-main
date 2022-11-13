from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from . import models


class BikeListSerializer(serializers.ModelSerializer):

    class Meta:

        model = models.Bike
        fields = ('model_number', 'price', 'is_purchased',)

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        representation['category'] = instance.category.name 
        representation['color'] = instance.color.name

        return representation


class AddBikeSerializer(serializers.Serializer):

    model_number = serializers.CharField(
        max_length=255,
        validators=[UniqueValidator(queryset=models.Bike.objects.all())]
    )
    category = serializers.CharField(max_length=255, required=True)
    color = serializers.CharField(max_length=255, required=True)
    price = serializers.FloatField(required=True)


    def validate(self, data):

        category = data.get('category')
        color = data.get('color')
        price = data.get('price')

        category_object = models.Category.objects.filter(name=category)
        color_object = models.Color.objects.filter(name=color)

        if category_object and color_object:
            pass
        else:
            msg = ('Category and Color should exist in database and should be in lower case')
            raise serializers.ValidationError(msg)

        if price < 0:
            msg = ('Price should be greated than 0')
            raise serializers.ValidationError(msg)

        data = {
            "model_number": data.get('model_number'),
            "category": category_object.first(),
            "color": color_object.first(),
            "price": price
        }

        return data


    def create(self, validated_data):

        bike_object = models.Bike.objects.create(
            model_number = validated_data['model_number'],
            category = validated_data['category'],
            color = validated_data['color'],
            price = validated_data['price']
        )

        return bike_object