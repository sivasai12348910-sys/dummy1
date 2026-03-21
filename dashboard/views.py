import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import SensorData

@csrf_exempt
def sensor_data_api(request):

    if request.method == "POST":
        try:
            temperature = request.POST.get("temperature")
            humidity = request.POST.get("humidity")
            soil = request.POST.get("soil_moisture")
            ph = request.POST.get("ph")

            image = request.FILES.get("image")

            SensorData.objects.create(
                temperature=temperature,
                humidity=humidity,
                soil_moisture=soil,
                ph=ph,
                image=image
            )

            return JsonResponse({"status": "stored"})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "POST only"}, status=405)


def dashboard_page(request):
    data = SensorData.objects.order_by("-created_at")
    return render(request, "dashboard.html", {"data": data})
