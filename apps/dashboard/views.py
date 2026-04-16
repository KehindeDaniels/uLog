from django.shortcuts import render, redirect
from django.utils import timezone
from datetime import datetime

from apps.core.models import Staff, Attendance
from apps.accounts.decorators import login_required



# DASHBOARD

@login_required
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



# ATTENDANCE LOGS

@login_required
def attendance_logs(request):
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



@login_required
def staff_management(request):
    error = None

    # ADD STAFF
    if request.method == "POST":
        staff_id = request.POST.get("staff_id", "").upper()
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        department = request.POST.get("department")

        if not staff_id or not full_name or not email:
            error = "All fields are required"

        elif Staff.objects.filter(staff_id=staff_id).exists():
            error = f"{staff_id} already exists"

        else:
            Staff.objects.create(
                staff_id=staff_id,
                full_name=full_name,
                email=email,
                department=department,
            )
            return redirect("/control/staff/")

    staff_list = Staff.objects.all().order_by("staff_id")

    return render(
        request,
        "dashboard/staff.html",
        {
            "staff_list": staff_list,
            "error": error,
            "active_page": "staff",
        },
    )


@login_required
def toggle_staff(request, staff_id):
    staff = Staff.objects.get(staff_id=staff_id)
    staff.is_active = not staff.is_active
    staff.save()

    return redirect("/control/staff/")