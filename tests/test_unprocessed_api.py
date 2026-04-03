import pytest
from django.core.files.base import ContentFile
from django.utils.timezone import now
from dashboard.models import SensorData

@pytest.mark.django_db
def test_get_unprocessed_valid(client):

    obj = SensorData.objects.create(
        reading_id="abc123",
        device_id="1",
        temperature=25,
        humidity=60,
        soil_moisture=1,
        ph=7,
        timestamp=now(),   # ✅ REQUIRED
        processed=False
    )

    obj.image.save("test.jpg", ContentFile(b"img"), save=True)

    response = client.get("/get-unprocessed/")

    assert response.status_code == 200
    data = response.json()["data"]

    assert len(data) == 1


@pytest.mark.django_db
def test_get_unprocessed_excludes_incomplete(client):
    SensorData.objects.create(
        reading_id="abc123",
        device_id="1",
        processed=False
        # missing fields → should be excluded
    )

    response = client.get("/get-unprocessed/")

    assert response.status_code == 200
    assert len(response.json()["data"]) == 0