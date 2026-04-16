from django.contrib import admin
from .models import Staff, Attendance

# Register your models here.
# admin.site.register(Staff)
# admin.site.register(Attendance)
# give a better display of staff in admin panel
class StaffAdmin(admin.ModelAdmin):
    list_display = ("staff_id", "full_name", "email", "department", "is_active")
    search_fields = ("staff_id", "full_name", "email")
    list_filter = ("department", "is_active")
admin.site.register(Staff, StaffAdmin)




class AttendanceAdmin(admin.ModelAdmin):
    list_display = ("staff", "date", "clock_in", "clock_out", "status")
    search_fields = ("staff__full_name", "staff__staff_id")
    list_filter = ("status", "date")
admin.site.register(Attendance, AttendanceAdmin)