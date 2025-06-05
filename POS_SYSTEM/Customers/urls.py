from django.urls import path
from .views import CustomersView, ListCustomersView

urlpatterns = [
    path("customers/", CustomersView.as_view(), name="customers"),
    path("customers/<int:id>/", CustomersView.as_view(), name="customers-detail"),
]