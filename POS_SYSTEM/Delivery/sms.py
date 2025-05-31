import africastalking
from django.conf import settings

username = settings.AFRICASTALKING_USERNAME
api_key = settings.AFRICASTALKING_API_KEY

africastalking.initialize(username, api_key)

sms = africastalking.SMS


# In transist message
# message = (
#     "Dear {customer_name}, your parcel with ID {parcel_id} is currently in transit. "
#     "It will be delivered to {delivery_address}. Thank you for choosing our service!"
# )
def parcel_in_transit_message(phone_number, message):
    try:
        response = sms.send(message, [phone_number])
        print("SMS response:", response)
        return response
    except Exception as e:
        print("Error sending SMS:", str(e))
        return None


def parcel_delivered_message(phone_number, message):
    try:
        response = sms.send(message, [phone_number])
        print("SMS response:", response)
        return response
    except Exception as e:
        print("Error sending SMS:", str(e))
        return None


def parcel_cancelled_message(phone_number, message):
    try:
        response = sms.send(message, [phone_number])
        print("SMS response:", response)
        return response
    except Exception as e:
        print("Error sending SMS:", str(e))
        return None
