from django.urls import path
from . import views

urlpatterns = [
    path('', views.select_portal, name='select_portal'),
    path('clock-in/', views.staff_id_entry, name='staff_id_entry'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('success/', views.success, name='success'),
]