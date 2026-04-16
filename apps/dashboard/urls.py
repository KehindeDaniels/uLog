from django.urls import path
from .views import attendance_logs, dashboard, toggle_staff, staff_management

urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("logs/", attendance_logs, name="attendance_logs"),
     path("staff/", staff_management),
    path("staff/toggle/<str:staff_id>/", toggle_staff),
]