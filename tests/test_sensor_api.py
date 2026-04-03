import pytest
from django.urls import reverse
import pytest
import json
from django.utils.timezone import now


@pytest.mark.django_db
def test_sensor_data_creation(client):
    response = client.post(
        "/sensor-data/",
        data=json.dumps({
            "device_id": "1",
            "reading_id": "abc123",
            "temperature": 25,
            "humidity": 60,
            "soil_moisture": 1,
            "ph": 7,
            "timestamp": now().isoformat()
        }),
        content_type="application/json"
    )

    assert response.status_code == 200
    assert response.json()["status"] == "sensor data stored"


@pytest.mark.django_db
def test_sensor_missing_fields(client):
    response = client.post(
        "/sensor-data/",
        data=json.dumps({}),
        content_type="application/json"
    )

    assert response.status_code == 400