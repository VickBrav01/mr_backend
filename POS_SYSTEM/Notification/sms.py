import africastalking
from django.conf import settings

# username = settings.AFRICASTALKING_USERNAME
# api_key = settings.AFRICASTALKING_API_KEY
username = "sandbox"
api_key = (
    "atsk_b681c4e4d2321ee49ce780d3c0912a5c8a760862d2db58ba9bdd5b34508ea18b43576cfa"
)


africastalking.initialize(username, api_key)

sms = africastalking.SMS


def delivery_message(message, phone_number):
    try:
        response = sms.send(message, [phone_number])
        print("SMS response:", response)
        return response
    except Exception as e:
        print("Error sending SMS:", str(e))
        return None


# def send_sms(phone_number, message):
#     try:
#         response = sms.send(message, [phone_number])
#         return response
#     except Exception as e:
#         return {"error": str(e)}
