from django.urls import path
from .views import ListAllDeliveries, CreateDelivery, RetrieveUpdateDelivery

urlpatterns = [
    path("deliveries/", ListAllDeliveries.as_view(), name="deliveries"),
    path("delivery/", CreateDelivery.as_view(), name="create-delivery"),
    path("delivery/<int:pk>/", RetrieveUpdateDelivery.as_view(), name="update-delivery"),
]
