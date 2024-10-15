from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import login, authenticate
from django.contrib.messages import get_messages
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import (
    LoginForm,
    SignupForm,
  
)

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
def Error404(request):
      return render(request, "page404.html")
def myteam(request):
      return render(request, "myteam.html")
@login_required
def dashboard(request):
      return render(request, "dashboard.html")
@login_required
def profile(request):
    return render(request, "profile.html")


# #update profile
# @login_required
# def profile(request):
#     if request.method == "POST":
#         form = UserProfileForm(request.POST, request.FILES, instance=request.user)
#         if form.is_valid():
#             user = form.save()
#             # Update session to prevent logout on password change
#             update_session_auth_hash(request, user)
#             messages.success(request, "Your profile was successfully updated.")
#             return redirect("profile")
#     else:
#         form = UserProfileForm(instance=request.user)

#     storage = get_messages(request)
#     for _ in storage:
#         pass
#     return render(request, "profile.html", {"form": form})

#addtask
@login_required
def addtask(request):
      return render(request, "addtask.html")
@login_required
def myteams(request):
      return render(request, "myteams.html")
@login_required
def resourceLib(request):
      return render(request, "resourceLib.html")



def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect("dashboard")
            else:
                messages.error(request, "Invalid email or password.")
    else:
        form = LoginForm()

    storage = get_messages(request)
    for _ in storage:
        pass
    return render(request, "login.html", {"form": form})


def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            return redirect("login")
    else:
        form = SignupForm()

    return render(request, "signup.html", {"form": form})

# @login_required
# def dashboard(request):
#     user = request.user
#     recent_goals = Goal.objects.filter(user=user).order_by("-created_at")[:5]
#     recent_attendance = Attendance.objects.filter(user=user).order_by("-date")[:5]
#     pending_leaves = Leave.objects.filter(user=user, status="PENDING")

#     context = {
#         "user": user,
#         "recent_goals": recent_goals,
#         "recent_attendance": recent_attendance,
#         "pending_leaves": pending_leaves,
#     }
#     return render(request, "dashboard.html", context)


