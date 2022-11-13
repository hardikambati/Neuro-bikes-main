from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework import permissions

from extensions.handler import SuccessResponse, FailureResponse
from . import serializers
from . import models

# Create your views here.


class UserTransactionView(APIView):
    
    """
        post : lets user buy a bike
        get : displays ordered bikes
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):

        serializer = serializers.UserTransactionSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return SuccessResponse("Bike purchased successfully", 200).response()


    def get(self, request):

        query = models.Order.objects.filter(user=request.user)

        if query:
            serializer = serializers.OrderListSerializer(query, many=True)
            return SuccessResponse(serializer.data, 200).response()

        return FailureResponse("No Bikes have been Ordered yet", 404).response()


class OrderCancellationView(APIView):

    """
        post : order cancellation request
        get : all cancelled orders list
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):

        serializer = serializers.OrderCancellationSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return SuccessResponse("Order Cancellation requested successfully", 200).response()

    
    def get(self, request):

        query = models.CancelledOrder.objects.filter(user=request.user)

        if query:
            serializer = serializers.CancelledOrderSerializer(query, many=True)
            return SuccessResponse(serializer.data, 200).response()

        return FailureResponse("No cancellation orders placed yet", 404).response()
