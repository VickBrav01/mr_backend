from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("Core.urls")),
    path("api/", include("Users.urls")),
    path("api/", include("Delivery.urls")),
    path("api/", include("Customers.urls")),
    path("api/", include("Payments.urls")),
]
