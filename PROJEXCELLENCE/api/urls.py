from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
  # path("", views.index, name="index"),
    # Authentication URLs
    path("", views.login_view, name="login"),
    path("login/", views.login_view, name="login"),
    path("logout/", LogoutView.as_view(next_page="login"), name="logout"),
    path("signup/", views.signup_view, name="signup"),
    path("Error404/", views.Error404, name="Error404"),
    path("myteam/", views.myteam, name="myteam"),
    path("dashboard/", views.dashboard, name="dashboard"),

    #task
    path("task/", views.task_list, name="task"),
    path('tasks/', views.tasks, name='tasks'), 
    path("task/add/", views.add_task, name="add_task"),
    path("task/<int:pk>/edit/", views.edit_task, name="edit_task"),
    path("task/<int:pk>/delete/", views.delete_task, name="delete_task"),

    path("myteams/", views.myteams, name="myteams"),
    path("resourceLib/", views.resourceLib, name="resourceLib"),

    #projects
    path("project/", views.project_list, name="project"),

    path("project/add/", views.add_project, name="add_project"),
    path("project/<int:pk>/edit/", views.edit_project, name="edit_project"),
    path("project/<int:pk>/delete/", views.delete_project, name="delete_project"),



    path("profile/", views.profile, name="profile"),
]