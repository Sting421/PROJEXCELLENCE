from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import login, authenticate
from django.contrib.messages import get_messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from .filters import TaskFilter

from .models import Task
from django.contrib import messages
from .forms import (
    LoginForm,
    SignupForm,
    TaskForm,
  
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



# ------------------------------------------- task -------------------------------------

@login_required
def tasks(request):
    # Get all tasks assigned to the logged-in user and order by 'assigned_to'
    tasks = Task.objects.filter(assigned_to=request.user).order_by('assigned_to')

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.assigned_to = request.user
            task.save()
            messages.success(request, 'Task added successfully.')
            return redirect('tasks')  # Redirect to the task list
    else:
        form = TaskForm()
    
    # Separate tasks into active and completed/expired based on status
    active_tasks = tasks.filter(status__in=['ACTIVE', 'IN_PROGRESS'])
    completed_expired_tasks = tasks.filter(status__in=['pending', 'EXPIRED'])

    return render(request, 'task.html', {
        'active_tasks': active_tasks,
        'completed_expired_tasks': completed_expired_tasks,
        'form': form
    })

@login_required
def task_list(request):
    # Fetch all tasks assigned to the current user, ordered by due date
    tasks = Task.objects.filter(assigned_to=request.user).order_by("-due_date")
    task_filter = TaskFilter(request.GET, queryset=tasks)

    paginator = Paginator(task_filter.qs, 10)  # Paginate the tasks, 10 per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Create a form instance for each task for editing purposes
    edit_task_forms = {task.id: TaskForm(instance=task) for task in tasks}

    context = {
        "page_obj": page_obj,
        "edit_task_forms": edit_task_forms,
        "add_task_form": TaskForm(),  # Form to add a new task
        "filter": task_filter,
    }
    return render(request, "task.html", context)# from task_list

@login_required
def add_task(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.assigned_to = request.user  # Assign the task to the logged-in user
            task.save()
            messages.success(request, "Task added successfully.")
            return redirect("tasks")
    else:
        form = TaskForm()
    return render(request, "task_add.html", {"form": form})

@login_required
def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk, assigned_to=request.user)
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Task deleted successfully.')
        return redirect('tasks')
    return render(request, 'delete_task.html', {'task': task})

@login_required
def edit_task(request, pk):
    # Fetch the task to be edited and ensure it belongs to the logged-in user
    task = get_object_or_404(Task, pk=pk, assigned_to=request.user)
    
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)  # Load form with task data
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated successfully.')
            return redirect('tasks')  # Redirect back to the tasks page
    else:
        form = TaskForm(instance=task)  # Load form with existing task data

    return render(request, 'task.html', {'form': form, 'task': task})


# ------------------------------------------- End of task -------------------------------------

