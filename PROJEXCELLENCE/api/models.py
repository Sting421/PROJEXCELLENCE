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
        ("PM", "projectmanger"),
        ("MEMBER", "member"),
    ]
    STATUS_CHOICES = [
        ("APPROVED", "Approved"),
        ("REJECTED", "Rejected"),
        ("PENDING", "Pending"),
    ]
    # Use email instead of username
    username = None  # Remove the username field entirely
    email = models.EmailField(_("email address"), unique=True)
    # Additional fields
    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{9,15}$",
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.",
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="EMPLOYEE")
    date_of_hire = models.DateField(blank=True, null=True)
    profile_path = models.ImageField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")
    # Override the groups field
    groups = models.ManyToManyField(
        "auth.Group",
        verbose_name=_("groups"),
        blank=True,
        related_name="custom_user_set",
        related_query_name="custom_user",
    )
    # Override the user_permissions field
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        verbose_name=_("user permissions"),
        blank=True,
        related_name="custom_user_set",
        related_query_name="custom_user",
    )
    objects = UserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "date_of_hire", "password"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    
    def save(self, *args, **kwargs):
        # Check if the profile picture has changed
        if self.pk:
            old_profile = User.objects.get(pk=self.pk)
            if old_profile.profile_path and old_profile.profile_path != self.profile_path:
                # Delete the old photo if it exists
                old_profile_path = os.path.join(settings.MEDIA_ROOT, old_profile.profile_path.name)
                if os.path.exists(old_profile_path):
                    os.remove(old_profile_path)
                # Rename the uploaded image to the current date and time
                if self.profile_path:
                    ext = os.path.splitext(self.profile_path.name)[1]
                    new_filename = timezone.now().strftime('%Y%m%d%H%M%S') + ext
                    self.profile_path.name = os.path.join('profiles', new_filename)
        super().save(*args, **kwargs)
        # Resize the image if it exists
        if self.profile_path and os.path.exists(self.profile_path.path):
            try:
                img = Image.open(self.profile_path.path)
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.profile_path.path)
            except FileNotFoundError:
                print(f"File not found: {self.profile_path.path}")


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
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
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
