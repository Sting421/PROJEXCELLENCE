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
    path("dashboard/", views.dashboard_view, name="dashboard"),
  
    #----------------   task   ----------------
    #path("task/", views.task_list, name="task"),
    path("task/<str:status>/", views.task_list, name="task"),
    path("tasks/add/", views.add_task, name="add_task"),
    path("task/<int:pk>/edit/", views.edit_task, name="edit_task"),
    path("task/<int:pk>/delete/", views.delete_task, name="delete_task"),
    
    #----------------   Resources   ----------------
    path("resourceLib/", views.resourceLib, name="resourceLib"),
    
    #----------------   Timeline   ----------------
    path("timeline/", views.timeline, name="timeline"),
    
    #----------------   Project   ----------------
    path("project/", views.project_list, name="project"),
    path("project/add/", views.add_project, name="add_project"),
    path("project/<int:pk>/edit/", views.edit_project, name="edit_project"),
    path("project/<int:pk>/delete/", views.delete_project, name="delete_project"),
      #Blog Post
    path("blogpost/<int:project_id>",views.blog_list,name="blog_post"),

    #Teams
    path("myteam/<int:project_id>/", views.team_list, name="team_list"),
    
    #----------------   Profile   ----------------
    path("profile/", views.edit_profile, name="profile"),
    path("profile/edit", views.edit_profile, name="edit_profile"),
    # path("profiles/uploadProfile", views.upload_profile, name ="upload_profile")
] 