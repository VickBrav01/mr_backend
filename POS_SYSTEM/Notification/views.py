# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.permissions import IsAuthenticated
# from Delivery.models import Delivery
# from django.shortcuts import get_object_or_404
# from Delivery.serializers import DeliverySerializer
# from .services import in_transit_message, delivered_message, canceled_message


# class MessageStatus(APIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = DeliverySerializer
#     queryset = Delivery.objects.all()

#     def post(self, request, *args, **kwargs):
#         pk = self.kwargs.get("pk")
#         try:
#             delivery = get_object_or_404(Delivery, pk=pk)
#             delivery_status = delivery.delivery_status

#             if delivery_status == "In Transit":
#                 in_transit_message(delivery)
#             elif delivery_status == "delivered":
#                 delivered_message(delivery)
#             elif delivery_status == "cancelled":
#                 canceled_message(delivery)

#             return Response({}, status=status.HTTP_200_OK)
#         except Exception as e:
#             response = {
#                 "error": str(e),
#                 "message": "An error occurred when updating the order",
#             }
#             return Response(data=response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
