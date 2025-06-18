from django.urls import path
from .views import BusinessDetailsView,DashboardStatsView

urlpatterns = [
    path('business-details/', BusinessDetailsView.as_view(), name='business-details-list'),
    path('dashboard/stats/', DashboardStatsView.as_view(), name='dashboard-stats'),

]