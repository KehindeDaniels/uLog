from django.shortcuts import render
from django.utils import timezone
from apps.core.models import Staff, Attendance


def dashboard(request):
    today = timezone.now().date()

    total_staff = Staff.objects.filter(is_active=True).count()

    today_records = Attendance.objects.filter(date=today)

    present = today_records.filter(status="present").count()
    late = today_records.filter(status="late").count()
    absent = total_staff - (present + late)

    context = {
        "total": total_staff,
        "present": present,
        "late": late,
        "absent": absent,
        "today_records": today_records,
        "today": today,
        "active_page": "dashboard",
    }

    return render(request, "dashboard/home.html", context)