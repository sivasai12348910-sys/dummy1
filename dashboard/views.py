import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import SensorData

@csrf_exempt
def sensor_data_api(request):
    if request.method == "POST":
        data = json.loads(request.body)

        SensorData.objects.create(
            temperature=data["temperature"],
            humidity=data["humidity"],
            soil_moisture=data["soil_moisture"],
            ph=data["ph"],
        )

        return JsonResponse({"status": "ok"})
    
    return JsonResponse({"error": "POST only"}, status=400)


def dashboard_page(request):
    data = SensorData.objects.order_by("-created_at")
    return render(request, "dashboard.html", {"data": data})
