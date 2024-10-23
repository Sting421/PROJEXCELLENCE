from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
import os
from django.conf import settings
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from PIL import Image
from django.contrib.auth.models import User



class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and return a superuser with an email and password."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    ROLE_CHOICES = [
        ("ADMIN", "Admin"),
        ("PROJECT_MANAGER", "Project Manager"),
        ("MEMBER", "Member"),
    ]

    STATUS_CHOICES = [
        ("APPROVED", "Approved"),
        ("REJECTED", "Rejected"),
        ("PENDING", "Pending"),
    ]

    email = models.EmailField(_("email address"), unique=True)
    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{9,15}$",
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.",
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    role = models.CharField(max_length=15, choices=ROLE_CHOICES, default="MEMBER")
    date_of_hire = models.DateField(blank=True, null=True)
    profile_path = models.ImageField(null=True, blank=True, upload_to='profiles/')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "date_of_hire"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        # Add your image handling logic here...
        super().save(*args, **kwargs)

class Project(models.Model):
    project_name = models.CharField(max_length=50)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.project_name
    

class Team(models.Model):
    team_name = models.CharField(max_length=50)
    users = models.ManyToManyField(User, through='TeamMembership')  # Define the through model
    project = models.ForeignKey('Project', on_delete=models.CASCADE)

    def __str__(self):
        return self.team_name

class TeamMembership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    role = models.CharField(max_length=50)
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} in {self.team.team_name} as {self.role}"



class ProjectManager(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} - {self.project}'


class BlogPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time_posted = models.DateTimeField(auto_now_add=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    message = models.TextField()

    def __str__(self):
        return f'{self.user} on {self.project}'


class Resources(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time_posted = models.DateTimeField(auto_now_add=True)
    filename = models.CharField(max_length=50)

    def __str__(self):
        return self.filename


class Admin(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=150)

    def __str__(self):
        return self.username


class File(models.Model):
    filename = models.CharField(max_length=50)
    time_posted = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    res = models.ForeignKey(Resources, on_delete=models.CASCADE)

    def __str__(self):
        return self.filename


class Task(models.Model):
    task_name = models.CharField(max_length=50)
    description = models.TextField()
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=50)
    due_date = models.DateTimeField()
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.task_name



class Member(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} joined on {self.time_posted}'


class Role(models.Model):
    role_name = models.CharField(max_length=50)
    permission = models.CharField(max_length=50)

    def __str__(self):
        return self.role_name


class TimeTracker(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE)
    date_started = models.DateTimeField()

    def __str__(self):
        return f'Time Tracker for {self.task} on {self.project}'
