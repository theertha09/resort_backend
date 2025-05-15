from rest_framework import generics
from .models import Resort, State
from .serializers import ResortSerializer, StateSerializer

# STATE VIEWS
class StateListCreateAPIView(generics.ListCreateAPIView):
    queryset = State.objects.all()
    serializer_class = StateSerializer

class StateRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = State.objects.all()
    serializer_class = StateSerializer
    lookup_field = 'id'

# RESORT VIEWS
class ResortListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ResortSerializer

    def get_queryset(self):
        queryset = Resort.objects.all()
        state_id = self.request.query_params.get('state_id')
        if state_id:
            queryset = queryset.filter(state__id=state_id)
        return queryset

class ResortRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Resort.objects.all()
    serializer_class = ResortSerializer
    lookup_field = 'id'
