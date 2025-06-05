from .views import Register, Login, Logout, UserView
from django.urls import path

urlpatterns = [
    path("register/", Register.as_view(), name="register"),
    path("login/", Login.as_view(), name="login"),
    path("logout/", Logout.as_view(), name="logout"),
    path("user/", UserView.as_view(), name="user"),

]