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

            SensorData.objects.create(
                temperature=temperature,
                humidity=humidity,
                soil_moisture=soil,
                ph=ph,
            )

            return JsonResponse({"status": "stored"})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "POST only"}, status=405)

@csrf_exempt
def upload_image(request):
    if request.method == "POST":
        image_data = request.body

        with open("media/latest.jpg", "wb") as f:
            f.write(image_data)

        return JsonResponse({"status": "image saved"})
def dashboard_page(request):
    data = SensorData.objects.order_by("-created_at")
    return render(request, "dashboard.html", {"data": data})
