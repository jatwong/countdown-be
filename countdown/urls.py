from django.urls import path
from .views import create_countdown, get_countdown

urlpatterns = [
    path("countdown/", create_countdown, name="create_countdown"),
    path("countdown/<int:id>/", get_countdown, name="get_countdown"),
]
