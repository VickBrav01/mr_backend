from .sms import delivery_message
from django.utils import timezone


def in_transit_message(delivery):
    delivery.delivery_status = "in_transit"
    delivery.save()

    message = f"Hi {delivery.customer_name}, your delivery #{delivery.parcel_id} has been receieved and it is In Transit. We shall notify you when it has arrived at the given destination"
    delivery_message(message, delivery.customer_phone)


def delivered_message(delivery):
    delivery.delivery_status = "delivered"
    delivery.delivered_at = timezone.now()
    delivery.save()

    message = f"Hi {delivery.customer_name}, your delivery #{delivery.parcel_id} has arrived at {delivery.delivery_address} {delivery.delivery_city}. Collect at any time"
    delivery_message(message, delivery.customer_phone)


def canceled_message(delivery):
    delivery.delivery_status = "cancelled"
    delivery.save()

    message = f"Hi {delivery.customer_name}, your delivery #{delivery.parcel_id} has been cancelled. Please contact us for more info"
    delivery_message(message, delivery.customer_phone)
