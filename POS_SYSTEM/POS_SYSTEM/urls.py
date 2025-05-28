from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("Core.urls")),
    path("api/", include("User.urls")),
]
