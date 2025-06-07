from django.urls import path
from .views import ReportsListView


urlpatterns = [
    path("reports/", ReportsListView.as_view(), name="reports"),
]
