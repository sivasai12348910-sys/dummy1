import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_datetime
from .models import SensorData
from django.core.files.base import ContentFile
from django.shortcuts import render

@csrf_exempt
def sensor_data_api(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST allowed"}, status=405)

    try:
        data = json.loads(request.body)

        device_id = data.get("device_id")
        reading_id = data.get("reading_id")

        if not device_id or not reading_id:
            return JsonResponse({"error": "device_id & reading_id required"}, status=400)

        obj, created = SensorData.objects.get_or_create(
            reading_id=reading_id,
            defaults={
                "device_id": device_id
            }
        )

        obj.temperature = data.get("temperature")
        obj.humidity = data.get("humidity")
        obj.soil_moisture = data.get("soil_moisture")
        obj.ph = data.get("ph")

        timestamp = data.get("timestamp")
        if timestamp:
            obj.timestamp = parse_datetime(timestamp)

        obj.save()

        return JsonResponse({
            "status": "sensor data stored",
            "reading_id": reading_id
        })

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def upload_image(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST allowed"}, status=405)

    try:
        device_id = request.GET.get("device_id")
        reading_id = request.GET.get("reading_id")

        if not device_id or not reading_id:
            return JsonResponse({"error": "device_id & reading_id required"}, status=400)

        # 🔥 read raw binary instead of FILES
        image_data = request.body

        if not image_data:
            return JsonResponse({"error": "No image data received"}, status=400)

        obj, created = SensorData.objects.get_or_create(
            reading_id=reading_id,
            defaults={"device_id": device_id}
        )

        # 🔥 Save manually to ImageField
        from django.core.files.base import ContentFile
        obj.image.save(f"{reading_id}.jpg", ContentFile(image_data))

        obj.save()

        return JsonResponse({
            "status": "image stored",
            "reading_id": reading_id
        })

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

def dashboard_page(request):
    data = SensorData.objects.order_by("-timestamp")
    return render(request, "dashboard.html", {"data": data})
