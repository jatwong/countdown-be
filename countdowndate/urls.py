from django.urls import path
from .views import create_countdown  # , #get_countdown

# <>/countdown/*
urlpatterns = [
    # get all countdowns
    # <>/countdowns/
    # path("create/", create_countdown, name="create_countdown"),
    
    # create new countdown
    # <>/countdowns/create/
    path("create/", create_countdown, name="create_countdown"),
    
    # edit a countdown
    # <>/countdowns/edit/id/
    # path("get/<int:id>/", get_countdown, name="get_countdown"),
    
    # delete a countdown
    # <>/countdowns/delete/id/
    # path("get/<int:id>/", get_countdown, name="get_countdown"),
]
