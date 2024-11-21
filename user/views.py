import json
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from django.middleware.csrf import get_token

from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

import user


def ping(request: HttpRequest) -> HttpResponse:
    return HttpResponse("pong")


def csrf(request: HttpRequest) -> JsonResponse:
    csrf_token = get_token(request=request)
    return JsonResponse({"csrf_token": csrf_token})


@require_http_methods(["POST"])
def register(request: HttpRequest) -> JsonResponse:
    try:
        # parse request
        data = json.loads(request.body)
        name = data.get("name")
        email = data.get("email")
        password = data.get("password")

        # validate inputs
        if name and email and password:
            # create user
            User.objects.create(
                first_name=name,
                username=email,
                email=email,
                password=make_password(password=password),
            )

    except KeyError:
        return HttpResponse("Invalid fields", status=400)
    except Exception as e:
        print("Failed", str(e))
        return HttpResponse("Internal server error", status=500)

    return JsonResponse(
        {
            "message": "Confirmed",
            "ok": True,
        },
        status=200,
    )


@require_http_methods(["POST"])
def login(request: HttpRequest) -> JsonResponse:
    try:
        data = json.loads(request.body)
        username = data["email"]
        password = data["password"]

        # check that username is in database
        # check password with hashed password
        # get user from database

    except KeyError:
        return HttpResponse("Invalid fields", status=400)
    except Exception as e:
        print("Failed", str(e))
        return HttpResponse("Internal server error", status=500)

    return JsonResponse(
        {
            "message": "Success",
            "ok": True,
            "user": user,
        }
    )
