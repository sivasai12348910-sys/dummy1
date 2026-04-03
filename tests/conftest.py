import pytest
from dashboard.models import SensorData

@pytest.fixture
def sensor_data(db):
    return SensorData.objects.create(
        reading_id="abc123",
        device_id="1",
        temperature=25,
        humidity=60,
        soil_moisture=1,
        ph=7,
        processed=False
    )