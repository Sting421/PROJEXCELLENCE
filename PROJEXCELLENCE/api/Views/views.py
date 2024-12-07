from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import login, authenticate
from django.contrib.messages import get_messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from ..filters import TaskFilter, ProjectFilter, TeamFilter
from django.contrib.auth.models import User
from django.urls import reverse
from django.db import models
from django.http import Http404
from django.utils import timezone
from datetime import datetime, timedelta
from calendar import monthcalendar, month_name, Calendar
import pytz
from ..models import Task ,Project, Team, TeamMembership, BlogPost, Comments, User
from django.contrib import messages
from django.contrib.auth.views import LogoutView
from ..forms import (
    LoginForm,
    SignupForm,
    TaskForm,
    ProjectForm,
    TeamForm,
    UserProfileForm,
    AddMemberForm,
    EditTaskForm,
    AddBlogForm,
    EditRoleForm,
    UploadProfile,
    EditAssigedTaskForm
    
)
from django.db.models import Q, Count

local_timezone = pytz.timezone('Asia/Manila') 

now_in_manila = datetime.now(local_timezone)
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
class CustomLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            print(f"User {request.user.email} logged out")
        return super().dispatch(request, *args, **kwargs)

@login_required
def timeline(request):
    # Get tasks
    tasks = Task.objects.filter(assigned_to=request.user).order_by("due_date")
    print(f"Number of tasks found: {tasks.count()}")  # Debug print

    current_date = datetime.now(local_timezone)
    year = int(request.GET.get('year', current_date.year))
    month = int(request.GET.get('month', current_date.month))
    current_day = current_date.day
    current_month = current_date.month
    current_year = current_date.year
   
    cal = Calendar(firstweekday=0)  

    calendar_data = []
    month_days = cal.monthdays2calendar(year, month)

    for week in month_days:
        processed_week = []
        for day, weekday in week:
            if day == 0:
                if len(processed_week) == 0:  
                    processed_week.append((day, 'prev-month'))
                else: 
                    processed_week.append((day, 'next-month'))
            else:
                processed_week.append((day, 'current-month'))
        calendar_data.append(processed_week)

    tasks_by_date = {}
    for task in tasks:
        if task.status != 'Done':
            date_key = (
            (task.due_date + timedelta(days=1)).strftime('%Y-%m-%d') 
            if task.due_date 
            else 'No Due Date'
)
                    
            if date_key not in tasks_by_date:
                tasks_by_date[date_key] = []
            tasks_by_date[date_key].append(task)

    for date_key, task_list in tasks_by_date.items():
        print(f"Date: {date_key}, Tasks: {[task.task_name for task in task_list]}")

    context = {
        'year': year,
        'month': month,
        'month_name': month_name[month],
        'current_day': current_day,
        'current_month': current_month,
        'current_year': current_year,
        'calendar_data': calendar_data,
        'tasks_by_date': tasks_by_date,
    }
    
    return render(request, 'timeline.html', context)

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
                user.isLogout = False
                user.save()
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
def task_details(request, pk):
    try:
        task = Task.objects.get(id=pk)
    except Task.DoesNotExist:
        raise Http404("Task not found") 
    
    if 'mark_done' in request.POST:
        task.status = 'Done'
        task.completed = True
        task.save()
        messages.success(request, "Task mark as done successfully!")
        return redirect('task_details', pk=pk)
    if 'undo_turn_in' in request.POST:
        task.status = 'On-going'
        task.completed = False
        task.save()
        messages.success(request, "Task mark as done successfully!")
        return redirect('task_details', pk=pk)
    if 'start_task' in request.POST:
        task.status = 'On-going'
        task.save()
        messages.success(request, "Task mark as done successfully!")
        return redirect('task_details', pk=pk)
    
    if task.assigned_to != request.user and task.created_by != request.user:
        raise Http404("You are not authorized to view this task")
    context = {
        "task": task  
    }
    return render(request, "taskDetails.html", context)


@login_required
def task_list(request,status):
    tasks = Task.objects.filter(assigned_to=request.user, status=status).order_by("due_date")
    task_filter = TaskFilter(request.GET, queryset=tasks)

    paginator = Paginator(task_filter.qs, 10)  
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    if 'start' in request.POST:
        task_id = request.POST.get('start')
        task = get_object_or_404(Task, id=task_id)
        task.status = 'On-going'
        task.date_started = timezone.now()
        task.save()
        messages.success(request, "Task Started successfully!")
        return redirect('task', status=task.status)

    edit_task_forms = {task.id: EditTaskForm(instance=task) for task in tasks}

    context = {
        "page_obj": page_obj,
        "edit_task_forms": edit_task_forms,
        "add_task_form": TaskForm(),  
        "filter": task_filter,
        'current_status': status
    }
    return render(request, "task.html", context)
@login_required
def task_list_project(request,status,project_id):
    tasks = Task.objects.filter(assigned_to=request.user, status=status, project_id=project_id).order_by("due_date")
    task_filter = TaskFilter(request.GET, queryset=tasks)

    paginator = Paginator(task_filter.qs, 10)  
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)


    edit_task_forms = {task.id: EditTaskForm(instance=task) for task in tasks}

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
        return redirect('task',status="Pending")
    return render(request, 'task.html', {'task': task})

@login_required
def edit_task(request, pk):
    task = get_object_or_404(Task, pk=pk, assigned_to=request.user)
    if request.method == 'POST':
        edit_form = EditTaskForm(request.POST, instance=task) 
        if edit_form.is_valid():
            if task.isAccepted:
                task.date_started = timezone.now() 
            edit_form.save()
            return redirect('task',status=task.status)  
    else:
        edit_form = EditTaskForm(instance=task)  

    return render(request, 'task.html', {'form': edit_form, 'task': task})

@login_required
def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.delete()
        return redirect('assign_task',status="Pending")
    return render(request, 'task.html', {'task': task})
@login_required
def edit_task_head(request, pk):
    task = get_object_or_404(Task, pk=pk)
    
    if request.method == 'POST':
        edit_form = EditAssigedTaskForm(request.POST, instance=task)
        if edit_form.is_valid():
            edit_form.save()
            messages.success(request, "Task updated successfully!")
            return redirect(reverse('assign_task', kwargs={'status': task.status}))
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        edit_form = EditAssigedTaskForm(instance=task)
    
    return render(request, 'assignTask.html', {'form': edit_form, 'task': task})


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


    tasks = Task.objects.filter(assigned_to=request.user).order_by("due_date")
    print(f"Number of tasks found: {tasks.count()}")  # Debug print

    current_date = datetime.now(local_timezone)
   
    year = int(request.GET.get('year', current_date.year))
    month = int(request.GET.get('month', current_date.month))
    current_day = current_date.day
    current_month = current_date.month
   
    cal = Calendar(firstweekday=0)  

    calendar_data = []
    month_days = cal.monthdays2calendar(year, month)
    print(current_date)
   
    
    for week in month_days:
        processed_week = []
        for day, weekday in week:
            if day == 0:
                if len(processed_week) == 0:  
                    processed_week.append((day, 'prev-month'))
                else: 
                    processed_week.append((day, 'next-month'))
            else:
                processed_week.append((day, 'current-month'))
        calendar_data.append(processed_week)

    tasks_by_date = {}
    for task in tasks:
        if task.status != 'Done':
            date_key = (
                (task.due_date + timedelta(days=1)).strftime('%Y-%m-%d') 
                if task.due_date 
                else 'No Due Date'
            )
            
            if date_key not in tasks_by_date:
                tasks_by_date[date_key] = []
            tasks_by_date[date_key].append(task)

    for date_key, task_list in tasks_by_date.items():
        print(f"Date: {date_key}, Tasks: {[task.task_name for task in task_list]}")
    context = {
       
        "projects": page_obj_projects,
        "tasks":page_obj_task,
        'year': year,
        'month': month,
        'month_name': month_name[month],
        'current_day': current_day,
        'current_month': current_month,
        'calendar_data': calendar_data,
        'tasks_by_date': tasks_by_date,
    }
    
    
    return render(request, 'dashboard.html', context)


#team
@login_required
def team_list(request, project_id):
    # Initialize forms at the start
    add_team_form = TeamForm(request.POST, current_user=request.user)
    add_member_form = AddMemberForm(request.POST, current_user=request.user)

    edit_role_form = EditRoleForm()
    user = request.user
    current_datetime = timezone.now()
    
 
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
    team_memberships_sorted = [
    (team, sorted(
        team.teammembership_set.all(),
        key=lambda m: (m.role != 'HEAD', m.role != 'MANAGER')
    ))
    for team in page_obj
]

  
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
        
        if 'delete_memeber' in request.POST:
            member_id = request.POST.get('user_id')
            team_id = request.POST.get('team_id')
            print("Member ID: ",member_id)
            try:
                memeber = TeamMembership.objects.get(id=member_id)
                memeber.delete()
                messages.success(request, 'Member remove successfully.')
                member_count = TeamMembership.objects.filter(team_id=team_id).count()
                # if member_count == 0:
                #     team = Team.objects.get(id=team_id, project_id=project_id)
                #     team.delete()
                #     messages.success(request, 'Team deleted as it has no members.')
                    
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
        
        if 'edit_member_role' in request.POST:
            print(request.POST)
            member_id = request.POST.get('user_id')
            membership = get_object_or_404(TeamMembership, id=member_id)
            
            edit_form = EditRoleForm(request.POST, instance=membership)
            print('Your role is: ',user_roles.get(membership.team_id))
            if edit_form.is_valid():
                edit_form.save()
                messages.success(request, "Member role updated successfully!")
            return redirect('team_list', project_id=project_id)
        if 'promte_member' in request.POST:
            print(request.POST)
            member_id = request.POST.get('user_id')
            membership = get_object_or_404(TeamMembership, id=member_id)
            
            membership.role = 'MANAGER'
            membership.save()
              
            messages.success(request, "Member role updated successfully!")
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
            
            add_member_form = AddMemberForm(request.POST, current_user=request.user,team=team)
            if add_member_form.is_valid():
                users = add_member_form.cleaned_data['users']
      
                
                for user in users:
                    if not TeamMembership.objects.filter(user=user, team=team).exists():
                        TeamMembership.objects.create(
                            user=user,
                            team=team,
                            project=project,
                           
                        )
                messages.success(request, "Members added successfully!")
                return redirect('team_list', project_id=project.id)
        elif 'add_member_by_email' in request.POST:
            team_id = request.POST.get('team_id')
            team = get_object_or_404(Team, id=team_id, project=project)
            get_email = request.POST.get('get_email')
            user = get_object_or_404(User, email = get_email)
            if not TeamMembership.objects.filter(user=user, team=team).exists():
                TeamMembership.objects.create(
                    user=user,
                    team=team,
                    project=project,
                    role=role
                )
                messages.success(request, "Members added successfully!")
            else:
                messages.error(request, "Members already on the team.")
            
            return redirect('team_list', project_id=project.id)

        elif 'assign_task' in request.POST:
            user_id = request.POST.get('user_id')
            due = request.POST.get('due-date')
            print("The due Date is:",due)
            user = get_object_or_404(User, id=user_id)
            assign_task = TaskForm(request.POST, project=project)
            if assign_task.is_valid():
                task = assign_task.save(commit=False)
                task.project_id = project
                task.assigned_to = user
                task.due_date = due
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
        "edit_role_form": edit_role_form,
        "team_memberships": team_memberships_sorted,
        "user_roles": user_roles,
        "current_datetime":current_datetime,
        
    }
    return render(request, "myteam.html", context)

@login_required
def edit_profile(request):
    upload_form = UploadProfile(request.POST, request.FILES, instance=request.user)
    edit_form = UserProfileForm(request.POST, request.FILES, instance=request.user, request=request)

    if request.method == 'POST':
       
        if 'upload_profile' in request.POST:
            if upload_form.is_valid():
                upload_form.save()
                return redirect('profile')  
     
        elif 'edit_profile' in request.POST:
            if edit_form.is_valid():
                current_password = edit_form.cleaned_data.get("current_password")
                if current_password and not request.user.check_password(current_password):
                   
                    edit_form.add_error('current_password', 'The current password is incorrect.')
                else:
                 
                    edit_form.save()
                    return redirect('profile') 

  
    else:
        upload_form = UploadProfile(instance=request.user)
        edit_form = UserProfileForm(instance=request.user, request=request)

    return render(request, 'profile.html', {
        'edit_form': edit_form,
        'upload_form': upload_form,
    })


def resource_library(request):
    if request.method == 'POST':
        print("Files:", request.FILES)  
        print("POST data:", request.POST)  
        
        title = request.POST.get('title')
        description = request.POST.get('description')
        category = request.POST.get('category')
        file = request.FILES.get('file')

        print(f"Title: {title}")  
        print(f"File: {file}")   

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


@login_required
def blog_list(request, project_id):
    add_blog_form = AddBlogForm()
    project = get_object_or_404(Project, id=project_id)
    blogs = BlogPost.objects.filter(project = project).order_by("-time_posted")
    if request.method == 'POST':
        if 'add_Post' in request.POST:
            post_id = request.POST.get('team_id')
            add_blog_form = AddBlogForm(request.POST)
            if add_blog_form.is_valid():
                blog = add_blog_form.save(commit=False)
                blog.project = project
                blog.posted_by = request.user
                blog.save()
                print("Terminal Confirmation: new Blog posted")
                messages.success(request, "Blog created successfully!")
                return redirect('blog_post', project_id=project.id)

        if 'edit_Post' in request.POST:
            post_id = request.POST.get('blog_id')
            print("The post Id : ",post_id)
            blog = get_object_or_404(BlogPost, id=post_id)
            new_message = request.POST.get('new_message')
            blog.message = new_message
            blog.save()
            return redirect('blog_post', project_id=project_id)

        if 'delete_Post' in request.POST:
            post_id = request.POST.get('blog_id')
            blog = get_object_or_404(BlogPost, id=post_id)
            blog.delete()
            return redirect('blog_post', project_id=project_id)
        
        if 'edit_Comment' in request.POST:
            post_id = request.POST.get('comment_id')
            print("The Comment Id : ",post_id)
            comment = get_object_or_404(Comments, id=post_id)
            new_message = request.POST.get('new_message')
            print("This is the new Comment: ", new_message)
            comment.text_comment = new_message
            comment.save()
            return redirect('blog_post', project_id=project_id)

        if 'delete_Comment' in request.POST:
            post_id = request.POST.get('comment_id')
            print("The Comment Id : ",post_id)
            comment = get_object_or_404(Comments, id=post_id)
            comment.delete()
            return redirect('blog_post', project_id=project_id)

        if 'add_comment' in request.POST:
            blog_id = request.POST.get('blog_id')
            text_comment = request.POST.get('text_comment')
            blog = get_object_or_404(BlogPost, id=blog_id)
            Comments.objects.create(user=request.user, blog=blog, project=project, text_comment=text_comment)
            messages.success(request, "Comment added successfully!")
            return redirect('blog_post', project_id=project_id)


    context = {
        "add_blog_form": AddBlogForm(),
        "project": project,  
        "blogs":blogs,
    }
    return render(request, "BlogPost.html", context)

@login_required
def assign_task(request,status):
    projects = Project.objects.filter(
    Q(created_by=request.user) | Q(teammembership__user=request.user), 
    task__created_by=request.user  # Use `task__created_by` to check tasks assigned by the user
    ).annotate(
        task_count=Count('task')
    ).filter(
        task_count__gt=0
    ).distinct()
    tasks = Task.objects.filter(created_by=request.user, status=status).order_by("due_date")
    task_filter = TaskFilter(request.GET, queryset=tasks)

    paginator = Paginator(task_filter.qs, 10)  
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)


    edit_task_forms = {task.id: EditAssigedTaskForm(instance=task) for task in tasks}

    context = {
        "page_obj": page_obj,
        "edit_task_forms": edit_task_forms,
        "add_task_form": TaskForm(),  
        "filter": task_filter,
        "current_status":status,
        'projects':projects,
    }
    return render(request, "assignTask.html", context)


@login_required
def due_day_task_List(request,year,month,day):
    tasks = Task.objects.filter(assigned_to=request.user).order_by("due_date")
    adjust_date = int(day) - 1
    date = f"{year}-{month:02d}-{adjust_date:02d}"
    return_date = f"{year}-{month:02d}-{day:02d}"
    
    current_date = datetime.now(local_timezone)
    years = int(request.GET.get('year', current_date.year))
    months = int(request.GET.get('month', current_date.month))
    current_day = current_date.day
    current_month = current_date.month
    current_year = current_date.year

    tasks_by_date = {}
    for task in tasks:
        if task.status != 'Done':
            date_key = (task.due_date ).strftime('%Y-%m-%d') if task.due_date else 'No Due Date'
            
            if date_key not in tasks_by_date:
                tasks_by_date[date_key] = []
            tasks_by_date[date_key].append(task)

    for date_key, task_list in tasks_by_date.items():
        print(f"Date: {date_key}, Tasks: {[task.task_name for task in task_list]}")

    context = {
        'tasks_by_date': tasks_by_date,
        'year': years,
        'month': months,
        'month_name': month_name[months],
        'current_day': current_day,
        'current_month': current_month,
        'current_year': current_year,
        'currdate':date,
        'getdate':return_date,
    }
    return render(request, "due_day_task_List.html", context)






