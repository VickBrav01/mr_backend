from django.urls import path
from .views import BusinessDetailsView

urlpatterns = [
    path('business-details/', BusinessDetailsView.as_view(), name='business-details-list'),
]