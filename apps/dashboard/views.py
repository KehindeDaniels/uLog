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




def attendance_logs(request):
    from datetime import datetime
    from django.utils import timezone

    date = request.GET.get("date")

    if date:
        selected_date = datetime.strptime(date, "%Y-%m-%d").date()
    else:
        selected_date = timezone.now().date()

    staff_list = Staff.objects.filter(is_active=True)

    records = Attendance.objects.filter(date=selected_date)

    table_data = []

    for staff in staff_list:
        record = records.filter(staff=staff).first()

        table_data.append({
            "staff": staff,
            "clock_in": record.clock_in if record else None,
            "clock_out": record.clock_out if record else None,
            "status": record.status if record else "absent",
        })

    present = sum(1 for r in table_data if r["status"] == "present")
    late = sum(1 for r in table_data if r["status"] == "late")
    absent = sum(1 for r in table_data if r["status"] == "absent")

    context = {
        "table_data": table_data,
        "selected_date": selected_date,
        "total": len(table_data),
        "present": present,
        "late": late,
        "absent": absent,
        "active_page": "logs",
    }

    return render(request, "dashboard/logs.html", context)