from django.urls import path
from .views import register, ping, csrf

# <>/user/*
urlpatterns = [
    # <>/user/register/
    path("register/", register, name="register"),
    path("ping/", ping, name="ping"),
    path("csrf/", csrf, name="csrf"),
    # <>/user/login/
    # path("login/", login, name="login"),
]
