from django.shortcuts import render, redirect
from django.utils import timezone
from apps.core.models import Staff, Attendance


def select_portal(request):
    return render(request, "clocking/select_portal.html")


def staff_id_entry(request):
    if request.method == "POST":
        staff_id = request.POST.get("staff_id", "").upper()

        try:
            staff = Staff.objects.get(staff_id=staff_id, is_active=True)

            # Store in session
            request.session["staff_id"] = staff.staff_id
            request.session["otp"] = "123456"

            return redirect("verify_otp")

        except Staff.DoesNotExist:
            return render(request, "clocking/staff_id.html", {
                "error": "Invalid Staff ID"
            })

    return render(request, "clocking/staff_id.html")


def verify_otp(request):
    staff_id = request.session.get("staff_id")

    if not staff_id:
        return redirect("staff_id_entry")

    staff = Staff.objects.get(staff_id=staff_id)

    if request.method == "POST":
        entered = request.POST.get("otp")
        expected = request.session.get("otp")

        if entered == expected:
            today = timezone.now().date()

            attendance, created = Attendance.objects.get_or_create(
                staff=staff,
                date=today
            )

            if not attendance.clock_in:
                attendance.clock_in = timezone.now()
                attendance.save()

            # Store success data
            request.session["success"] = {
                "name": staff.full_name,
                "id": staff.staff_id,
                "time": timezone.now().strftime("%H:%M:%S"),
            }

            return redirect("success")

        return render(request, "clocking/otp.html", {
            "staff": staff,
            "error": "Invalid OTP"
        })

    return render(request, "clocking/otp.html", {"staff": staff})


def success(request):
    data = request.session.get("success")

    if not data:
        return redirect("staff_id_entry")

    # clear session
    request.session.flush()

    return render(request, "clocking/success.html", data)