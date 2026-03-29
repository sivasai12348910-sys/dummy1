import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_datetime
from django.utils.timezone import now
from django.shortcuts import render
from django.core.files.base import ContentFile
from .models import SensorData


# =========================
# SENSOR DATA API
# =========================
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
            defaults={"device_id": device_id}
        )

        # ✅ Always update (important for merging)
        obj.device_id = device_id
        obj.temperature = data.get("temperature")
        obj.humidity = data.get("humidity")
        obj.soil_moisture = data.get("soil_moisture")
        obj.ph = data.get("ph")

        # ✅ Timestamp handling (robust)
        timestamp = data.get("timestamp")
        parsed = parse_datetime(timestamp) if timestamp else None

        if parsed:
            obj.timestamp = parsed
        else:
            obj.timestamp = now()  # fallback

        obj.save()

        return JsonResponse({
            "status": "sensor data stored",
            "reading_id": reading_id
        })

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


# =========================
# IMAGE UPLOAD API (RAW ESP32)
# =========================
@csrf_exempt
def upload_image(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST allowed"}, status=405)

    try:
        device_id = request.GET.get("device_id")
        reading_id = request.GET.get("reading_id")

        if not device_id or not reading_id:
            return JsonResponse({"error": "device_id & reading_id required"}, status=400)

        image_data = request.body

        if not image_data:
            return JsonResponse({"error": "No image data received"}, status=400)

        obj, created = SensorData.objects.get_or_create(
            reading_id=reading_id,
            defaults={"device_id": device_id}
        )

        # ✅ ensure mapping consistency
        obj.device_id = device_id

        # ✅ save image properly
        obj.image.save(f"{reading_id}.jpg", ContentFile(image_data), save=False)

        obj.save()

        return JsonResponse({
            "status": "image stored",
            "reading_id": reading_id
        })

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


# =========================
# DASHBOARD
# =========================
def dashboard_page(request):
    data = SensorData.objects.order_by("-timestamp", "-id")
    return render(request, "dashboard.html", {"data": data})


# =========================
# GET UNPROCESSED DATA (AI PULL)
# =========================
@csrf_exempt
def get_unprocessed_data(request):
    try:
        readings = SensorData.objects.filter(
            processed=False,
            image__isnull=False,
            temperature__isnull=False
        )[:10]

        # ✅ lock records immediately (prevents duplicates)
        ids = [r.id for r in readings]
        SensorData.objects.filter(id__in=ids).update(processed=True)

        data = []

        for r in readings:
            data.append({
                "reading_id": r.reading_id,
                "device_id": r.device_id,
                "temperature": r.temperature,
                "humidity": r.humidity,
                "soil_moisture": r.soil_moisture,
                "ph": r.ph,
                "timestamp": str(r.timestamp) if r.timestamp else None,
                "image_url": request.build_absolute_uri(r.image.url) if r.image else None
            })

        return JsonResponse({"data": data})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


# =========================
# UPDATE RESULT (FROM AI)
# =========================
@csrf_exempt
def update_result(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST allowed"}, status=405)

    try:
        if not request.body:
            return JsonResponse({"error": "Empty body"}, status=400)

        data = json.loads(request.body)

        reading_id = data.get("reading_id")

        if not reading_id:
            return JsonResponse({"error": "reading_id required"}, status=400)

        try:
            obj = SensorData.objects.get(reading_id=reading_id)
        except SensorData.DoesNotExist:
            return JsonResponse({"error": "Invalid reading_id"}, status=404)

        # ✅ update AI results
        obj.disease = data.get("disease", "Unknown")
        obj.stress = data.get("stress", "Unknown")
        obj.decision = data.get("decision", "No decision")

        obj.processed = True  # mark completed

        obj.save()

        return JsonResponse({"status": "updated"})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)