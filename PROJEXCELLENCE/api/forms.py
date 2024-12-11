from django import forms
from django.contrib.auth import get_user_model 
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Task, Project, Team, TeamMembership, BlogPost
from django.utils.timezone import make_aware, is_naive, localtime
from datetime import datetime
from django.contrib.auth import authenticate
import pytz



manila_timezone = pytz.timezone("Asia/Manila")

User = get_user_model()


class LoginForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")



class SignupForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"}), label="Password"
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        label="Confirm Password",
    )
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "password",
        ]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
        }
        labels = {
            "first_name": "First Name",
            "last_name": "Last Name",
            "email": "Email",
            "password": "Password",
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            self.add_error("password_confirm", "Passwords do not match")

        return cleaned_data
    

class UserProfileForm(forms.ModelForm):
    current_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "id": "current_password"}),
        label="Current Password",
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "id": "new_password"}),
        label="New Password",
        required=False,
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "id": "confirm_password"}),
        label="Confirm New Password",
        required=False,
    )
    

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "current_password",
            "new_password",
            "confirm_password",
        ]
    def __init__(self, *args, **kwargs):
        # Pop request from kwargs and save it for later use
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        
        # Pre-fill user fields if request and user are available
        if self.request and self.request.user.is_authenticated:
            self.initial['first_name'] = self.request.user.first_name
            self.initial['last_name'] = self.request.user.last_name
            self.initial['email'] = self.request.user.email

        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.attrs = {"enctype": "multipart/form-data"}
        self.helper.add_input(Submit("submit", "Update Profile"))

        


    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")
        current_password = cleaned_data.get("current_password")

        # Check if current password is correct
        if current_password:
            if not self.request.user.check_password(current_password):
                raise forms.ValidationError("The current password is incorrect.")

        if new_password and new_password != confirm_password:
            raise forms.ValidationError("The new passwords do not match.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)

        # Handle password change
        new_password = self.cleaned_data.get("new_password")
        if new_password:
            user.set_password(new_password)
        if commit:
            user.save()
        return user

class UploadProfile(forms.ModelForm):
 

    class Meta:
        model = User
        fields = [
            "profile_path",
        ]
    def __init__(self, *args, **kwargs):
        # Pop request from kwargs and save it for later use
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.attrs = {"enctype": "multipart/form-data"}
        self.helper.add_input(Submit("submit", "Update Profile"))

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["task_name", "description"]
        widgets = {
            "task_name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
           
        }
        labels = {
            "task_name": "Task Name",
            "description": "Task Description",
        }

    def __init__(self, *args, project=None, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk and self.instance.due_date:
            # Ensure the initial value is formatted to exclude seconds
            self.fields["due_date"].initial = (
                localtime(self.instance.due_date).strftime("%Y-%m-%dT%H:%M")
            )

    def clean_due_date(self):
        due_date = self.cleaned_data.get("due_date")
        if due_date:
            # Convert naive to aware if needed
            if is_naive(due_date):
                due_date = make_aware(due_date)
            if due_date < localtime():
                raise forms.ValidationError("Due date cannot be in the past")
        return due_date

    
class EditTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["status"]
class EditAssigedTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['task_name','status','description']
      
class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['project_name', 'description']  
        widgets = {
            'project_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Project Name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Project Description', 'rows': 5}),
        }
 
# class TeamForm(forms.ModelForm):
#     class Meta:
#         model = Team
#         fields = ['team_name', 'users', 'project']
        
  
#     team_name = forms.CharField(
#         label="Team Name",
#         max_length=50,
#         widget=forms.TextInput(attrs={'class': 'form-control'})
#     )
    
#     users = forms.ModelMultipleChoiceField(
#         queryset=User.objects.all(),
#         widget=forms.CheckboxSelectMultiple, 
#         label="Select Team Members"
#     )
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
       
#         self.fields['project'].queryset = Project.objects.filter(id)

class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['team_name', 'users']
  
  
    team_name = forms.CharField(
        label="Team Name",
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    users = forms.ModelMultipleChoiceField(
        queryset=User.objects.none(),
        widget=forms.CheckboxSelectMultiple, 
        label="Select Team Members"
    )
    role = forms.ChoiceField(
        choices=TeamMembership.ROLE_CHOICES,
        label="Select Role",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    def __init__(self, *args, **kwargs):
        current_user = kwargs.pop('current_user', None)  # Extract the current user
        super().__init__(*args, **kwargs)
        
        if current_user:
            self.fields['users'].queryset = User.objects.exclude(id=current_user.id)
        else:
            # Fallback to include all users if current_user is not provided
            self.fields['users'].queryset = User.objects.all()


class AddMemberForm(forms.Form):
    users = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Select Members"
    )
    

    def __init__(self, *args, **kwargs):
        current_user = kwargs.pop('current_user', None) 
        team = kwargs.pop('team', None)  
        super().__init__(*args, **kwargs)

       
        if current_user:
            self.fields['users'].queryset = User.objects.exclude(id=current_user.id)
        else:
            self.fields['users'].queryset = User.objects.all()

        if team:
             existing_members = team.users.all()  
             self.fields['users'].queryset = self.fields['users'].queryset.exclude(id__in=existing_members.values_list('id', flat=True))
        self.fields['users'].queryset = self.fields['users'].queryset.order_by('first_name')
class EditRoleForm(forms.ModelForm):
    class Meta:
        model = TeamMembership  
        fields = ['role'] 
        widgets = {
            'role': forms.Select(attrs={"class": "form-control"}), 
        }
        labels = {
            'role': "Role", 
        }


class AddBlogForm(forms.ModelForm):
    class Meta:
        model = BlogPost  
        fields = ['message']