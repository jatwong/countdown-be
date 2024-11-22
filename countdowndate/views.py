from datetime import datetime
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
import json

from django.db import DatabaseError

from countdowndate.models import CountdownDate
import user


@require_http_methods(["GET"])
def list_countdowns(request: HttpRequest) -> JsonResponse:
    """
    list_countdowns handles GET requests to list all countdowns for a specific user.
    Retrieves user cookie to identify user and get user_id from the database.

    Args:
        request (HttpRequest): The HTTP request object containing user cookies.

    Returns JsonResponse:
            200 (success) and list of user's countdowns and status
        or errors:
            401 (unauthorized user)
            400 (missing content/fields)
            500 (database error) and db error message
    """
    user_token = request.COOKIES.get("jwt")  # TODO: get the user's jwt token

    # TODO: find user via token
    # user = get_user()

    if not user:
        return JsonResponse({"message": "401 Unauthorized"}, status=401)

    # get user's db user_id
    # user_id = user.user_id

    # get all the user's countdowns
    try:
        countdowns = CountdownDate.objects.filter(user_id=user_id).values(
            "id",
            "title",
            "date",
        )

        # converst QuerySet object to list for frontend
        countdowns_list = list(countdowns)

        return JsonResponse(
            {"countdowns": countdowns_list},
            status=200,
        )
    except DatabaseError as e:  # database error
        return JsonResponse(
            {"message": "Internal server error", "error": str(e)},
            status=500,
        )


@require_http_methods(["POST"])
def create_countdown(request: HttpRequest) -> JsonResponse:
    """
    create_countdown handles POST requests to create a new countdown for a user.
    Retrieves user cookie to identify user and get user_id from the database.
    Includes user_id when creating new countdown.

    Args:
        request (HttpRequest): The HTTP request object containing user cookies.
            body: includes title and date of countdown

    Returns JsonResponse:
            201 (success) with new countdown id and status
        or errors:
            401 (unauthorized user)
            400 (missing content/fields)
            500 (database error) and db error message
    """
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
    """
    edit_countdown handles POST requests to edit a countdown with a given id for a user.
    Retrieves user cookie to identify user and get user_id from the database.

    Args:
        request (HttpRequest): The HTTP request object containing user cookies.
            body: includes title and date of countdown
        id (int): The id of the countdown to be edited

    Returns JsonResponse:
            200 (success) with updated countdown and status
        or errors:
            401 (unauthorized user)
            400 (missing content/fields)
            404 (countdown not found)
            500 (database error) and db error message
    """
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
    """
    delete_countdown handles DELETE requests to delete a countdown with a given id for a user.
    Retrieves user cookie to identify user and get user_id from the database.

    Args:
        request (HttpRequest): The HTTP request object containing user cookies.
        id (int): The id of the countdown to be deleted

    Returns JsonResponse:
            200 (success) with status
        or errors:
            401 (unauthorized user)
            404 (countdown not found)
            500 (database error) and db error message
    """
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
