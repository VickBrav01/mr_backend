from .views import Register, Login, Logout,UserProfileView
from django.urls import path

urlpatterns = [
    path("register/", Register.as_view(), name="register"),
    path("login/", Login.as_view(), name="login"),
    path("profile/", UserProfileView.as_view(), name="user_profile"),
    path("logout/", Logout.as_view(), name="logout"),
]
