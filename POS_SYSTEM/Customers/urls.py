from django.urls import path
from .views import ListCustomersView


urlpatterns = [path("customers/", ListCustomersView.as_view(), name="customers")]
