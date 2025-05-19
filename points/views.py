# points/views.py

from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import Points
from .serializers import PointsNumberSerializer

class PointsListCreateAPIView(generics.ListCreateAPIView):
    queryset = Points.objects.all()
    serializer_class = PointsNumberSerializer
    permission_classes = [AllowAny]

class PointsRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Points.objects.all()
    serializer_class = PointsNumberSerializer
    permission_classes = [AllowAny]
    lookup_field = 'user__uuid'  # lookup by the related user's UUID

    def get_object(self):
        # Override to get Points object by user's UUID
        uuid = self.kwargs.get('uuid')
        return self.queryset.get(user__uuid=uuid)
