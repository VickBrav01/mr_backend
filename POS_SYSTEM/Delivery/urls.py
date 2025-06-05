from django.urls import path
from .views import ListAllDeliveries, CreateDelivery, UpdateDelivery,DeleteDelivery

urlpatterns = [
    path("deliveries/", ListAllDeliveries.as_view(), name="deliveries"),
    path("delivery/", CreateDelivery.as_view(), name="create-delivery"),
    path("delivery/<int:pk>", UpdateDelivery.as_view(), name="update-delivery"),
    path("delivery/<int:pk>/delete", DeleteDelivery.as_view(), name="delete-delivery"),
]
