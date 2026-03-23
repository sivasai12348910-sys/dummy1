from django.urls import path
from .views import sensor_data_api, dashboard_page,upload_image,get_unprocessed_data,update_result


urlpatterns = [
    path("sensor-data/", sensor_data_api),
    path("upload_image/",upload_image),
    path("get-unprocessed/",get_unprocessed_data),
    path("update-result/",update_result),
    path("", dashboard_page),
] 
