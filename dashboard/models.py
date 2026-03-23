from django.db import models

class SensorData(models.Model):
    device_id = models.CharField(max_length=100)
    reading_id = models.CharField(max_length=100, unique=True)

    temperature = models.FloatField(null=True, blank=True)
    humidity = models.FloatField(null=True, blank=True)
    soil_moisture = models.IntegerField(null=True, blank=True)
    ph = models.FloatField(null=True, blank=True)

    image = models.ImageField(upload_to="leaves/", null=True, blank=True)

    timestamp = models.DateTimeField(null=True, blank=True)

    processed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.device_id} - {self.reading_id}"
