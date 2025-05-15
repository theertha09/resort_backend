# # address/views.py
# from rest_framework import generics,status
# from rest_framework.permissions import AllowAny
# from .serializers import BulkReferralSerializer
# from .models import Referral
# from rest_framework.response import Response  # ✅ Required for returning JSON responses


# class BulkListCreateAPIView(generics.GenericAPIView):
#     serializer_class = BulkReferralSerializer
#     permission_classes = [AllowAny]

#     def post(self, request, *args, **kwargs):
#         data = request.data

#         # Accept both single and multiple entries
#         if isinstance(data, dict):
#             data = [data]

#         serializer = self.get_serializer(data=data, many=True)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()

#         return Response(serializer.data, status=status.HTTP_201_CREATED)
