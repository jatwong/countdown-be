from datetime import datetime
from django.shortcuts import get_object_or_404
from django.http import HttpRequest, JsonResponse
from django.views.decorators.http import require_http_methods
import json


@require_http_methods(["POST"])
def create_countdown(request: HttpRequest) -> JsonResponse:
    try:
        data = json.loads(request.body)
        title = data["title"]
        # target_date = data["target_date"]
        description = data["description"]

        # countdown = Countdown.objects.create(
        #     title=title, target_date=target_date, description=description
        # )

        # Mock response
        return JsonResponse(
            {
                "id": 1,
                "title": title,
                "date": datetime.now(),
                "description": description,
            },
            status=201,
        )

    except KeyError:
        return JsonResponse({"error": "Missing required fields"}, status=400)


# Retrieve Countdown Entry
def get_countdown(request: HttpRequest, id: int) -> JsonResponse:

    # Mock response
    return JsonResponse(
        {
            "id": 1,
            "title": "Some title",
            "date": datetime.now(),
            "description": "Some description",
        }
    )
