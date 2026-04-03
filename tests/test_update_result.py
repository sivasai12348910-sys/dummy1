import pytest
import json
from dashboard.models import SensorData

@pytest.mark.django_db
def test_update_result_success(client):

    obj = SensorData.objects.create(
        reading_id="abc123",
        device_id="1",
        processed=False
    )

    response = client.post(
        "/update-result/",
        data=json.dumps({"reading_id": "abc123"}),  # ✅ correct key
        content_type="application/json"
    )

    assert response.status_code == 200

    obj.refresh_from_db()
    assert obj.processed is True


@pytest.mark.django_db
def test_update_result_missing_id(client):
    response = client.post(
        "/update-result/",
        data=json.dumps({}),
        content_type="application/json"
    )

    assert response.status_code == 400


@pytest.mark.django_db
def test_update_result_invalid_id(client):
    response = client.post(
        "/update-result/",
        data=json.dumps({"reading_id": "wrong"}),
        content_type="application/json"
    )

    assert response.status_code == 404