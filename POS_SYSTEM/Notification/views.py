# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.permissions import IsAuthenticated

# from .sms import send_sms


# class SendSMSView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         phone_number = request.data.get("phone_number")
#         message = request.data.get("message")

#         if not phone_number or not message:
#             return Response(
#                 {"error": "phone_number and message are required."},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         result = send_sms(phone_number, message)
#         return Response(result, status=200)
