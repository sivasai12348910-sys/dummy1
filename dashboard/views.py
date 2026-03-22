import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import SensorData
from django.core.files.base import ContentFile

@csrf_exempt
def sensor_data_api(request):

    if request.method == "POST":
        try:
            data = json.loads(request.body)

            SensorData.objects.create(
                device_id=data.get("device_id"),
                temperature=data.get("temperature"),
                humidity=data.get("humidity"),
                soil_moisture=data.get("soil_moisture"),
                ph=data.get("ph"),
            )

            return JsonResponse({"status": "sensor stored"})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "POST only"}, status=405)

@csrf_exempt
def upload_image(request):

    if request.method == "POST":
        try:
            device_id = request.GET.get("device_id")

            if not device_id:
                return JsonResponse({"error": "device_id missing"}, status=400)

            obj = SensorData.objects.filter(device_id=device_id).last()

            if not obj:
                return JsonResponse({"error": "No matching sensor data"}, status=404)

            image_file = ContentFile(request.body, name=f"{device_id}.jpg")

            obj.image.save(f"{device_id}.jpg", image_file)
            obj.save()

            return JsonResponse({"status": "image saved"})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "POST only"}, status=405)

def dashboard_page(request):
    data = SensorData.objects.order_by("-created_at")
    return render(request, "dashboard.html", {"data": data})
