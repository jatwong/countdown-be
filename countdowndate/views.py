from datetime import datetime
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
import json

from psycopg import DatabaseError

from countdowndate.models import CountdownDate
import user


@require_http_methods(["GET"])
def list_countdowns(request: HttpRequest) -> JsonResponse:
    user_token = request.COOKIES.get("jwt")  # TODO: get the user's jwt token

    # TODO: find user via token
    # user = get_user()


@require_http_methods(["POST"])
def create_countdown(request: HttpRequest) -> JsonResponse:
    data = json.loads(request.body)
    user_token = request.COOKIES.get("jwt")  # TODO: get the user's jwt token
    title = data.get("title")
    date = data.get("date")

    # TODO: find user via token
    # user = get_user()

    # if invalid user/no authorization
    if not user:
        return JsonResponse(
            {"message": "401 Unauthorized"},
            status=401,
        )

    try:
        if title and date:
            CountdownDate.objects.create(
                user_id=123,  # TODO: get user id
                title=title,
                date=date,
            )
            return JsonResponse(
                {
                    "message": "Countdown created",
                    "countdown_id": 1,
                },
                status=201,
            )
        else:  # user bad request
            return JsonResponse(
                {"message": "Missing fields"},
                status=400,
            )
    except DatabaseError as e:  # database error
        return JsonResponse(
            {"message": "Internal server error", "error": str(e)},
            status=500,
        )


@require_http_methods(["[POST]"])
def edit_countdown(request: HttpRequest, id: int) -> JsonResponse:
    data = json.loads(request.body)
    user_token = request.COOKIES.get("jwt")  # TODO: get the user's jwt token
    title = data.get("title")
    date = data.get("date")

    # TODO: find user via token
    # user = get_user()

    # user not authorized
    if not user:
        return JsonResponse(
            {"message": "401 Unauthorized"},
            status=401,
        )

    # check if countdown is in the database before updating
    try:
        countdown = CountdownDate.objects.get(id=id)

        if title and date:
            countdown.update(
                title=title,
                date=date,
            )
        else:  # user bad request
            return JsonResponse(
                {"message": "Invalid content"},
                status=400,
            )

        return JsonResponse(
            {
                "message": "Countdown updated",
                "countdown": {
                    "id": id,
                    "title": title,
                    "date": date,
                },
            },
            status=200,
        )
    except CountdownDate.DoesNotExist:  # record not found
        return JsonResponse(
            {"message": "Countdown not found"},
            status=404,
        )
    except DatabaseError as e:  # database error
        return JsonResponse(
            {"message": "Internal server error", "error": str(e)},
            status=500,
        )


@require_http_methods(["DELETE"])  # TODO: update FE to use delete method?
def delete_countdown(request: HttpRequest, id: int) -> JsonResponse:
    user_token = request.COOKIES.get("jwt")  # TODO: get the user's jwt token

    # TODO: find user via token
    # user = get_user()

    # user not authorized
    if not user:
        return JsonResponse(
            {"message": "401 Unauthorized"},
            status=401,
        )

    # check if countdown is in the database before deleting
    try:
        countdown = CountdownDate.objects.get(id=id)
        countdown.delete()

        return JsonResponse(
            {"message": "Countdown successfully deleted"},
            status=200,
        )
    except CountdownDate.DoesNotExist:  # record not found
        return JsonResponse(
            {"message": "Countdown not found"},
            status=404,
        )
    except DatabaseError as e:  # database error
        return JsonResponse(
            {"message": "Internal server error", "error": str(e)},
            status=500,
        )
