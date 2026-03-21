from django.urls import path
from .views import sensor_data_api, dashboard_page


urlpatterns = [
    path("sensor-data/", sensor_data_api),
    path("", dashboard_page),
] 
