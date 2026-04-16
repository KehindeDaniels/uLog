from django.shortcuts import render, redirect


def login_view(request):
    # If already logged in → go to dashboard
    if request.session.get("is_authenticated"):
        return redirect("/control/")

    error = None

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        if email == "admin@uba.com" and password == "Isaiah@2048":
            request.session["is_authenticated"] = True
            request.session["user_email"] = email
            return redirect("/control/")
        else:
            error = "Invalid email or password"

    return render(request, "accounts/login.html", {"error": error})


def logout_view(request):
    request.session.flush()
    return redirect("/login/")