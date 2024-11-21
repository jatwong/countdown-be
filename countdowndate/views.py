from datetime import datetime
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
import json

from countdowndate.models import CountdownDate
import user


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
        return JsonResponse({"message": "401 Unauthorized"}, status=401)

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
    else:
        return JsonResponse(
            {"message": "Missing fields"},
            status=400,
        )


@require_http_methods(["[POST]"])
def edit_countdown(request: HttpRequest, id: int) -> JsonResponse:
    data = json.loads(request.body)
    user_token = request.COOKIES.get("jwt")  # TODO: get the user's jwt token
    title = data.get("title")
    date = data.get("date")

    # TODO: find user via token
    # user = get_user()

    if not user:
        return JsonResponse({"message": "401 Unauthorized"}, status=401)

    if title and date:
        CountdownDate.objects.update_or_create
        # Entry.objects.filter(id=10).update(comments_on=False)

        return JsonResponse(
            {
                "message": "Countdown updated",
                "countdown": {
                    "id": id,
                    "title": title,
                    "date": date,
                },
            }
        )
