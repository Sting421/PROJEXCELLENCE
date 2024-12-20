from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .Views import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
  # path("", views.index, name="index"),
    # Authentication URLs
    path("", views.landing, name='landing'),
    path("test/", views.test, name='test'),
    path("login/", views.login_view, name="login"),
    path("logout/", LogoutView.as_view(template_name="logout.html"), name="logout"),
    path("signup/", views.signup_view, name="signup"),
    path("Error404/", views.Error404, name="Error404"),
    path("dashboard/", views.dashboard_view, name="dashboard"),
  
    #----------------   task   ----------------
    #path("task/", views.task_list, name="task"),
    path("task/<str:status>/", views.task_list, name="task"),

    
    path("assign_task/<str:status>/", views.assign_task, name="assign_task"),
    path("due_day_task_List/<int:year>/<int:month>/<int:day>/", views.due_day_task_List, name="due_day_task_List"),

    path("task/<str:status>/<int:project_id>/", views.task_list_project, name="task_project"),
    path("tasks/add/", views.add_task, name="add_task"),
    path("task/<int:pk>/edit/", views.edit_task, name="edit_task"),
    path("taskHead/<int:pk>/edit/", views.edit_task_head, name="edit_task_byAssigned"),
    path("taskHead/<int:pk>/delete/", views.delete_task, name="delete_task_byAssiged"),
    path("task/<int:pk>/delete/", views.delete_task, name="delete_task"),

    path("task_details/<int:pk>/", views.task_details, name="task_details"),
    
    #----------------   Resources   ----------------
    path("resourceLib/", views.resourceLib, name="resourceLib"),
    
    #----------------   Timeline   ----------------
    path("timeline/", views.timeline, name="timeline"),

    path("timeline/<int:project_id>/", views.timelinePMview, name="timelinePM"),
    
    #----------------   Project   ----------------
    path("project/", views.project_list, name="project"),
    path("project/add/", views.add_project, name="add_project"),
    path("project/<int:pk>/edit/", views.edit_project, name="edit_project"),
    path("project/<int:pk>/delete/", views.delete_project, name="delete_project"),
    
    #----------------   Blog Post   ----------------
    path("blogpost/<int:project_id>",views.blog_list,name="blog_post"),

    #----------------    Teams    ----------------
    path("myteam/<int:project_id>/", views.team_list, name="team_list"),
    
    #----------------   Profile   ----------------
    path("profile/", views.edit_profile, name="profile"),
    path("profile/edit", views.edit_profile, name="edit_profile"),
    # path("profiles/uploadProfile", views.upload_profile, name ="upload_profile")
] 