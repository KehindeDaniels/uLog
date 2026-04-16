from django.urls import path
from .views import attendance_logs, dashboard

urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("logs/", attendance_logs, name="attendance_logs"),
]