from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
  # path("", views.index, name="index"),
    # Authentication URLs
    path("login/", views.login_view, name="login"),
    path("logout/", LogoutView.as_view(next_page="login"), name="logout"),
    path("signup/", views.signup_view, name="signup"),
    path("Error404/", views.Error404, name="Error404"),
    path("myteam/", views.myteam, name="myteam"),
    path("dashboard/", views.dashboard, name="dashboard"),

    path("addtask/", views.addtask, name="addtask"),
    path("myteams/", views.myteams, name="myteams"),
    path("resourceLib/", views.resourceLib, name="resourceLib"),


    path("profile/", views.profile, name="profile"),
]