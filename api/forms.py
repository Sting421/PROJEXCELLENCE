from django import forms
from django.contrib.auth import get_user_model 
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Task, Project, Team, TeamMembership, BlogPost
from django.utils import timezone
from datetime import datetime
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
    new_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "id": "new_password"}
        ),
        label="New Password",
        required=False,
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "id": "confirm_password"}
        ),
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
            "date_of_hire",
            "profile_path",
            'new_password',
            'confirm_password',
        ]
        widgets = {
            "date_of_hire": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.attrs = {"enctype": "multipart/form-data"}
        self.helper.add_input(Submit("submit", "Update Profile"))

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password and new_password != confirm_password:
            raise forms.ValidationError("The new passwords do not match.")

        return cleaned_data

    def save(self, commit=True):
      
        user = super().save(commit=False)

        new_password = self.cleaned_data.get("new_password")
        if new_password:
            user.set_password(new_password)

        if not self.cleaned_data.get("profile_path"):
            user.profile_path = self.instance.profile_path

        if commit:
            user.save()

        return user





class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["task_name", "description", "due_date"]
        widgets = {
            "task_name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
            "due_date": forms.DateTimeInput(attrs={"type": "datetime-local", "class": "form-control"}),
        }
        labels = {
            "task_name": "Task Name",
            "description": "Task Description",
            "due_date": "Due Date",
        }

    def __init__(self, *args, project=None, **kwargs):
        super().__init__(*args, **kwargs)

    def clean_due_date(self):
        due_date = self.cleaned_data.get("due_date")
        if due_date and due_date < timezone.now():
            raise forms.ValidationError("Due date cannot be in the past")
        return due_date
    
class EditTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["status"]
      
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
    role = forms.ChoiceField(
        choices=TeamMembership.ROLE_CHOICES,
        widget=forms.Select(attrs={"class": "form-control"}),
        label="Role"
    )
    def __init__(self, *args, **kwargs):
        current_user = kwargs.pop('current_user', None)  # Extract the current user
        super().__init__(*args, **kwargs)
        
        if current_user:
            self.fields['users'].queryset = User.objects.exclude(id=current_user.id)
            print("test",self.fields['users'].queryset)
        else:
            self.fields['users'].queryset = User.objects.all()
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