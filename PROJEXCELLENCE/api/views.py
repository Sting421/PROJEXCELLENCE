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
from django.utils import timezone


from .models import Task ,Project, Team, TeamMembership, Resource
from django.contrib import messages
from .forms import (
    LoginForm,
    SignupForm,
    TaskForm,
    ProjectForm,
    TeamForm,
    UserProfileForm,
    AddMemberForm,
    
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
def timeline(request):
    return render(request, "timeline.html")

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
            task.created_by = request.user
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
        return redirect('task',status="On-going")
    return render(request, 'delete_task.html', {'task': task})

@login_required
def edit_task(request, pk):
    
    task = get_object_or_404(Task, pk=pk, assigned_to=request.user)
    
    if request.method == 'POST':
        edit_form = TaskForm(request.POST, instance=task) 
        if edit_form.is_valid():
            if task.isAccepted:
                task.date_started = timezone.now() 
            edit_form.save()
            return redirect('task',status=task.status)  
    else:
        edit_form = TaskForm(instance=task)  

    return render(request, 'task.html', {'form': edit_form, 'task': task})


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
    page_obj_task = paginator.get_page(page_number)

    paginator = Paginator(projects, 2)
    page_number = request.GET.get('page')
    page_obj_projects = paginator.get_page(page_number)
    context = {
       
        "projects": page_obj_projects,
        "tasks":page_obj_task,
    }
    
    return render(request, 'dashboard.html', context)

#team
@login_required
def team_list(request, project_id):
    # Initialize forms at the start
    add_team_form = TeamForm()
    add_member_form = AddMemberForm()
    user = request.user
    

    project = get_object_or_404(Project, id=project_id)
    # Initialize TaskForm with project
    assign_task = TaskForm(project=project)
    
    teams = Team.objects.filter(project=project).order_by("-id").prefetch_related('teammembership_set')
    team_filter = TeamFilter(request.GET, queryset=teams)
    paginator = Paginator(team_filter.qs, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Get user roles for all teams
    user_roles = {
        membership.team_id: membership.role 
        for membership in TeamMembership.objects.filter(
            user=request.user,
            project=project
        )
    }

    if request.method == 'POST':
        if 'delete_team' in request.POST:
            team_id = request.POST.get('team_id')
            try:
                team = Team.objects.get(id=team_id, project_id=project_id)
                # Optional: Add permission check
                if request.user == team.project.created_by:
                    team.delete()
                    messages.success(request, 'Team deleted successfully.')
                else:
                    messages.error(request, 'You do not have permission to delete this team.')
            except Team.DoesNotExist:
                messages.error(request, 'Team not found.')
            return redirect('team_list', project_id=project_id)

        if 'edit_team' in request.POST:
            team_id = request.POST.get('team_id')
            team = get_object_or_404(Team, id=team_id)
            new_name = request.POST.get('team_name')
            team.team_name = new_name
            team.save()
            return redirect('team_list', project_id=project_id)
            
        # Handle team creation
        elif 'team_name' in request.POST:
            add_team_form = TeamForm(request.POST, current_user=request.user)
            if add_team_form.is_valid():
                team = add_team_form.save(commit=False)
                team.project = project
                team.save()
                
                users = add_team_form.cleaned_data.get('users', [])
                role = add_team_form.cleaned_data.get('role')
                for user in users:
                    if not TeamMembership.objects.filter(user=user, team=team, project=project).exists():
                        TeamMembership.objects.create(
                            user=user, 
                            team=team, 
                            project=project, 
                            role=role
                        )
                messages.success(request, "Team created successfully!")
                return redirect('team_list', project_id=project.id)
        
        # Handle member addition
        elif 'add_member' in request.POST:
            team_id = request.POST.get('team_id')
            team = get_object_or_404(Team, id=team_id, project=project)
            add_member_form = AddMemberForm(request.POST, current_user=request.user)
            
            if add_member_form.is_valid():
                users = add_member_form.cleaned_data['users']
                role = add_member_form.cleaned_data['role']
                
                for user in users:
                    if not TeamMembership.objects.filter(user=user, team=team).exists():
                        TeamMembership.objects.create(
                            user=user,
                            team=team,
                            project=project,
                            role=role
                        )
                messages.success(request, "Members added successfully!")
                return redirect('team_list', project_id=project.id)

        elif 'assign_task' in request.POST:
           
            assign_task = TaskForm(request.POST, project=project)
            if assign_task.is_valid():
                task = assign_task.save(commit=False)
                task.project_id = project
                task.created_by = request.user
              
                task.save()
                messages.success(request, "Task assigned successfully!")
                return redirect('team_list', project_id=project.id)
            else:
                messages.error(request, "Error assigning task. Please check the form.")

    context = {
        "page_obj": page_obj,
        "add_team_form": add_team_form,
        "add_member_form": add_member_form,
        "assign_task":assign_task,
        "filter": team_filter,
        "project": project,
        "team_memberships": [(team, team.teammembership_set.all()) for team in page_obj],
        "user_roles": user_roles,
    }
    return render(request, "myteam.html", context)

@login_required
def edit_profile(request):
    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Your profile was successfully updated.")
            return redirect("profile")
    else:
        form = UserProfileForm(instance=request.user)
    storage = get_messages(request)
    
    for _ in storage:
        pass
    return render(request, "profile.html", {"form": form})

def resource_library(request):
    if request.method == 'POST':
        print("Files:", request.FILES)  # Debug print
        print("POST data:", request.POST)  # Debug print
        
        title = request.POST.get('title')
        description = request.POST.get('description')
        category = request.POST.get('category')
        file = request.FILES.get('file')

        print(f"Title: {title}")  # Debug print
        print(f"File: {file}")    # Debug print

        if title and description and category and file:
            try:
                resource = Resource.objects.create(
                    title=title,
                    description=description,
                    category=category,
                    file=file
                )
                print(f"Resource created: {resource}")  # Debug print
                messages.success(request, 'Resource uploaded successfully!')
                return redirect('resource_library')
            except Exception as e:
                print(f"Error creating resource: {e}")  # Debug print
                messages.error(request, f'Upload failed: {str(e)}')
        else:
            messages.error(request, 'Please fill all required fields')

    featured_resources = Resource.objects.filter(featured=True)[:4]
    resources = Resource.objects.all().order_by('-uploaded_at')[:4]

    context = {
        'featured_resources': featured_resources,
        'resources': resources,
    }
    return render(request, 'resourceLib.html', context)

