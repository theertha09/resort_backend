from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Reservation
from .serializers import ReservationSerializer
from django.shortcuts import get_object_or_404


class ReservationCreateAPIView(APIView):
    permission_classes = []
    authentication_classes = []

    def get(self, request):
        reservations = Reservation.objects.all()
        serializer = ReservationSerializer(reservations, many=True)
        return Response({
            "code": status.HTTP_200_OK,
            "message": "Success",
            "result": serializer.data
        }, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ReservationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "code": status.HTTP_201_CREATED,
                "message": "Reservation created successfully",
                "result": [serializer.data]
            }, status=status.HTTP_201_CREATED)
        return Response({
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "Validation errors",
            "result": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class ReservationDetailAPIView(APIView):
    def get_object(self, pk):
        return get_object_or_404(Reservation, pk=pk)

    def get(self, request, pk):
        reservation = self.get_object(pk)
        serializer = ReservationSerializer(reservation)
        return Response({
            "code": status.HTTP_200_OK,
            "message": "Success",
            "result": [serializer.data]
        }, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        reservation = self.get_object(pk)
        serializer = ReservationSerializer(reservation, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "code": status.HTTP_200_OK,
                "message": "Reservation updated successfully",
                "result": [serializer.data]
            }, status=status.HTTP_200_OK)
        return Response({
            "code": status.HTTP_400_BAD_REQUEST,
            "message": "Validation errors",
            "result": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        reservation = self.get_object(pk)
        reservation.delete()
        return Response({
            "code": status.HTTP_204_NO_CONTENT,
            "message": "Reservation deleted successfully",
            "result": [f"Reservation ID {pk} deleted"]
        }, status=status.HTTP_204_NO_CONTENT)
