from django.db import models

class SensorData(models.Model):
    device_id = models.CharField(max_length=50)

    temperature = models.FloatField()
    humidity = models.FloatField()
    soil_moisture = models.IntegerField()
    ph = models.FloatField()

    image = models.ImageField(upload_to='sensor_images/', null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
