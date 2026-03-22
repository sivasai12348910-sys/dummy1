from django.urls import path
from .views import sensor_data_api, dashboard_page,upload_image


urlpatterns = [
    path("sensor-data/", sensor_data_api),
    path("upload_image/",upload_image),
    path("", dashboard_page),
] 
