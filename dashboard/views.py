import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import SensorData

@csrf_exempt
def sensor_data_api(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            SensorData.objects.create(
                temperature=data.get("temperature"),
                humidity=data.get("humidity"),
                soil_moisture=data.get("soil_moisture"),
                ph=data.get("ph"),
            )

            return JsonResponse({"status": "stored"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "POST only"}, status=405)


def dashboard_page(request):
    data = SensorData.objects.order_by("-created_at")
    return render(request, "dashboard.html", {"data": data})
