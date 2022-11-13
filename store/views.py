from rest_framework.views import APIView
from . import serializers
from rest_framework.authtoken.models import Token
from rest_framework import permissions

from extensions.permissions import IsAdminUser
from extensions.handler import SuccessResponse, FailureResponse
from . import models

# Create your views here.

class StaffAccessView(APIView):

    permission_classes = (IsAdminUser,)

    def post(self, request):

        serializer = serializers.AddBikeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return SuccessResponse(serializer.data, 200).response()


class BikeListView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):

        query = models.Bike.objects.filter(is_purchased=False)

        if query:
            serializer = serializers.BikeListSerializer(query, many=True)
            return SuccessResponse(serializer.data, 200).response()

        return FailureResponse("No bikes available to purchase", 404).response()