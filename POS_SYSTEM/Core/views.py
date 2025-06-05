# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.request import Request
# from rest_framework import status
# from rest_framework.permissions import IsAuthenticated
# <<<<<<< HEAD
# from .models import BusinessModel
# =======
# from .models import BusinessDetails
# >>>>>>> f8e31858df6a145db361a14d0245205d67b0fef0
# from .serializers import BusinessDetailsSerializer  # You should already have this


# class BusinessDetailsView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request: Request, *args, **kwargs):
#         try:
# <<<<<<< HEAD
#             business = BusinessModel.objects.first()
# =======
#             business = BusinessDetails.objects.first()
# >>>>>>> f8e31858df6a145db361a14d0245205d67b0fef0
#             if not business:
#                 return Response({"detail": "No business found."}, status=204)

#             serializer = BusinessDetailsSerializer(business)
#             return Response(serializer.data, status=200)

#         except Exception as e:
#             return Response({"error": str(e)}, status=500)

#     def post(self, request: Request, *args, **kwargs):
# <<<<<<< HEAD
#         instance = BusinessModel.objects.first()
# =======
#         instance = BusinessDetails.objects.first()
# >>>>>>> f8e31858df6a145db361a14d0245205d67b0fef0
#         if instance:
#             data = self.request.data
#             serializer = BusinessDetailsSerializer(instance, data=data, partial=True)
#         else:
#             serializer = BusinessDetailsSerializer(data=data)

#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=200)

#         return Response(serializer.errors, status=400)
