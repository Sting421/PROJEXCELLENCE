from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import login, authenticate
from django.contrib.messages import get_messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from .filters import TaskFilter, ProjectFilter, TeamFilter
from django.contrib.auth.models import User
from django.urls import reverse
from django.db import models
from django.http import Http404

from .models import Task ,Project, Team, TeamMembership
from django.contrib import messages
from .forms import (
    LoginForm,
    SignupForm,
    TaskForm,
    ProjectForm,
    TeamForm,
    EditProfile,
  
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
@login_required
def timeline(request):
    return render(request, "timeline.html")


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
def myteams(request):
      return render(request, "myteam.html")
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
        form = LoginForm()

    # storage = get_messages(request)
    # for _ in storage:
    #     pass
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

# ------------------------------------------- task -------------------------------------
# @login_required
# def task_list(request):
#     tasks = Task.objects.filter(assigned_to=request.user).order_by("-due_date")
#     task_filter = TaskFilter(request.GET, queryset=tasks)

#     paginator = Paginator(task_filter.qs, 10)  
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)


#     edit_task_forms = {task.id: TaskForm(instance=task) for task in tasks}

#     context = {
#         "page_obj": page_obj,
#         "edit_task_forms": edit_task_forms,
#         "add_task_form": TaskForm(),  
#         "filter": task_filter,
#     }
#     return render(request, "task.html", context)
# @login_required
# def add_task(request):
#     if request.method == "POST":
#         form = TaskForm(request.POST)
#         if form.is_valid():
#             task = form.save(commit=False) 
#             task.save() 
#             return redirect("task",)  
#     else:
#         form = TaskForm()
    
#     return render(request, "add_task.html", {"form": form})

# @login_required
# def delete_task(request, pk):
#     task = get_object_or_404(Task, pk=pk, assigned_to=request.user)
#     if request.method == 'POST':
#         task.delete()
#         # messages.success(request, 'Task deleted successfully.')
#         return redirect('task')
#     return render(request, 'delete_task.html', {'task': task})

# @login_required
# def edit_task(request, pk):
    
#     task = get_object_or_404(Task, pk=pk, assigned_to=request.user)
    
#     if request.method == 'POST':
#         form = TaskForm(request.POST, instance=task) 
#         if form.is_valid():
#             form.save()
#             # messages.success(request, 'Task updated successfully.')
#             return redirect('task')  
#     else:
#         form = TaskForm(instance=task)  

#     return render(request, 'task.html', {'form': form, 'task': task})


# task filter team_list

@login_required
def task_list(request,status):
    tasks = Task.objects.filter(assigned_to=request.user, status=status).order_by("due_date")
    task_filter = TaskFilter(request.GET, queryset=tasks)

    paginator = Paginator(task_filter.qs, 10)  
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)


    edit_task_forms = {task.id: TaskForm(instance=task) for task in tasks}

    context = {
        "page_obj": page_obj,
        "edit_task_forms": edit_task_forms,
        "add_task_form": TaskForm(),  
        "filter": task_filter,
    }
    return render(request, "task.html", context)

@login_required
def add_task(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False) 
            task.save() 
            return redirect("task",status=task.status)  
    else:
        form = TaskForm()
    
    return render(request, "add_task.html", {"form": form})

@login_required
def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk, assigned_to=request.user)
    if request.method == 'POST':
        task.delete()
        # messages.success(request, 'Task deleted successfully.')
        return redirect('task',status="On-going")
    return render(request, 'delete_task.html', {'task': task})

@login_required
def edit_task(request, pk):
    
    task = get_object_or_404(Task, pk=pk, assigned_to=request.user)
    
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task) 
        if form.is_valid():
            form.save()
            # messages.success(request, 'Task updated successfully.')
            return redirect('task',status=task.status)  
    else:
        form = TaskForm(instance=task)  

    return render(request, 'task.html', {'form': form, 'task': task})




# ------------------------------------------- End of task -------------------------------------


#------------------------------------------- projects -------------------------------------

@login_required
def projects(request):
    # Get all projects created by the logged-in user and order by 'project_name'
    projects = Project.objects.filter(created_by=request.user).order_by('project_name')

    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.created_by = request.user
            project.save()
            # messages.success(request, 'Project added successfully.')
            return redirect('project')

    else:
        form = ProjectForm()
    
    return render(request, 'project.html', {
        'projects': projects,
        'form': form
    })

@login_required
def project_list(request):
    projects = Project.objects.filter(models.Q(created_by=request.user) | models.Q(teammembership__user=request.user)).distinct()
    project_filter = ProjectFilter(request.GET, queryset=projects)

    paginator = Paginator(project_filter.qs, 8)  # Paginate the projects, 5 per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    edit_project_forms = {project.id: ProjectForm(instance=project) for project in projects}

    context = {
        "page_obj": page_obj,
        "edit_project_forms": edit_project_forms,
        "add_project_form": ProjectForm(), 
        "filter": project_filter,
        "projects":projects,
    }
    return render(request, "project.html", context)

@login_required
def add_project(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.created_by = request.user
            project.save()
            # messages.success(request, "Project added successfully.")
            return redirect("project")
    else:
        form = ProjectForm()
    return render(request, "add_project.html", {"form": form})

@login_required
def delete_project(request, pk):
    try:
        project = get_object_or_404(Project, pk=pk, created_by=request.user)
        if request.method == 'POST':
            project.delete()
            return redirect('project')
        return render(request, 'delete_project.html', {'project': project})
    except Http404:
            return redirect('Error404')

@login_required
def edit_project(request, pk):
    try:
        project = get_object_or_404(Project, pk=pk, created_by=request.user)
        
        if request.method == 'POST':
            form = ProjectForm(request.POST, instance=project)  
            if form.is_valid():
                form.save()
            
                return redirect('project') 
        else:
            form = ProjectForm(instance=project)  #

        return render(request, 'project_edit.html', {'form': form, 'project': project})
    except Http404:
        return redirect('Error404')
#------------------------------------------- end projects -------------------------------------


@login_required
def dashboard_view(request):
    projects = Project.objects.filter(models.Q(created_by=request.user) | models.Q(teammembership__user=request.user)).distinct()
    tasks = Task.objects.filter(assigned_to=request.user)
    
   
    paginator = Paginator(tasks, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        "page_obj": page_obj,
        "projects": projects,
    }
    
    return render(request, 'dashboard.html', context)

#team
@login_required
def team_list(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    #teams = Team.objects.filter(project=project).filter(id=10).order_by("-id") #for static testing
    teams = Team.objects.filter(project=project).order_by("-id")
    team_filter = TeamFilter(request.GET, queryset=teams)
    paginator = Paginator(team_filter.qs, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    if request.method == 'POST':
        add_team_form = TeamForm(request.POST)
        if add_team_form.is_valid():
            team = add_team_form.save(commit=False)
            team.project = project  
            team.save()
            
            # Handle adding users with a default role
            for user in add_team_form.cleaned_data['users']:
                TeamMembership.objects.create(user=user, team=team,project_id =project ,  role='member')  # Default role
            return redirect('team_list', project_id=project.id)
    else:
        add_team_form = TeamForm()

    edit_team_forms = {team.id: TeamForm(instance=team) for team in page_obj}

    # Fetching team memberships for each team on the current page
    team_memberships = {team.id: team.teammembership_set.all() for team in page_obj}

    context = {
        "page_obj": page_obj,
        "edit_team_forms": edit_team_forms,
        "add_team_form": add_team_form,  
        "filter": team_filter,
        "project": project,
        "team_memberships": team_memberships,  # Add this line to include memberships
    }

    return render(request, "myteam.html", context)

def edit_profile(request):
    if request.method == 'POST':
        form = EditProfile(request.POST)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to the list of teams
        
    else:  
        form = EditProfile()
    return render(request, 'myteam.html', {'add_team_form': form})

