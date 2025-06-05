from django.urls import path
from .views import PaymentsListView

urlpatterns = [
    path("payments/", PaymentsListView.as_view(), name="payments"),
]
