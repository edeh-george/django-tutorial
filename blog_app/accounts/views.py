from django.contrib.auth import authenticate, get_user_model, login, logout
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import redirect

from .forms import LoginForm

User = get_user_model()


def login_view(request):
    if request.method == "GET":
        return render(request, "auth/login.html", {"form": LoginForm()})
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            try:
                user = authenticate(username=username, password=password)
                if user:
                    login(request, user)
                    redirect("user_detail", id=str(user.id))
                else:
                    return HttpResponse("Invalid credentials", status=401)

            except User.DoesNotExist:
                return HttpResponse("")

        else:
            return HttpResponse("Provide information matching checks", 400)


def logout_view(request):
    logout(request)
    return redirect("login")
