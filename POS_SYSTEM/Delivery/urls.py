from django.urls import path
from .views import ListAllDeliveries, CreateDelivery, RetrieveUpdateDelivery, InitiateMpesaPayment
from .callback import mpesa_callback

urlpatterns = [
    path("deliveries/", ListAllDeliveries.as_view(), name="deliveries"),
    path("delivery/", CreateDelivery.as_view(), name="create-delivery"),
    path("delivery/<int:pk>/", RetrieveUpdateDelivery.as_view(), name="update-delivery"),
    path("delivery/<int:pk>/pay/", InitiateMpesaPayment.as_view(), name="initiate-mpesa-payment"),
    path("mpesa/callback/", mpesa_callback, name="mpesa-callback"),
]