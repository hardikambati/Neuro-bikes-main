from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework import permissions

from extensions.handler import SuccessResponse, FailureResponse
from . import serializers
from . import models

# Create your views here.

class BookServicing(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):

        serializer = serializers.BookServiceSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return SuccessResponse("Servicing Booked Successfully", 200).response()


    def get(self, request):

        query = models.ServiceOrder.objects.filter(user=request.user)

        if query:
            serializer = serializers.ServiceSerializer(query, many=True)
            return SuccessResponse(serializer.data, 200).response()

        return FailureResponse("No service history", 404).response()