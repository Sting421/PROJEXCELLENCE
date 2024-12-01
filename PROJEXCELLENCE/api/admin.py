from django.contrib import admin
from .models import (
    User,
    Project,
    Team,
    TeamMembership,
    BlogPost,
    Comments,
    Resources,
    File,
    Task,
    Resource,
)

# Customize the User admin
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name')
    search_fields = ('email', 'first_name', 'last_name')
    

# Customize the Project admin
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('project_name', 'description', 'created_by', 'date_created')
    search_fields = ('project_name', 'description')
    list_filter = ('date_created',)
    ordering = ('-date_created',)

# Customize the Team admin
@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('team_name', 'project')
    search_fields = ('team_name',)
    list_filter = ('project',)

# Customize the TeamMembership admin
@admin.register(TeamMembership)
class TeamMembershipAdmin(admin.ModelAdmin):
    list_display = ('user', 'team', 'role', 'joined_at')
    search_fields = ('user__email', 'team__team_name', 'role')
    list_filter = ('role', 'joined_at')

# Customize the BlogPost admin
@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('posted_by', 'time_posted', 'project', 'message')
    search_fields = ('message',)
    list_filter = ('time_posted',)

# Customize the Comments admin
@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ('user', 'blog', 'time_posted', 'project', 'text_comment')
    search_fields = ('text_comment',)
    list_filter = ('time_posted',)

# Customize the Resources admin
@admin.register(Resources)
class ResourcesAdmin(admin.ModelAdmin):
    list_display = ('user', 'filename', 'time_posted')
    search_fields = ('filename',)
    list_filter = ('time_posted',)

# Customize the File admin
@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ('filename', 'user', 'res', 'time_posted')
    search_fields = ('filename',)
    list_filter = ('time_posted',)

# Customize the Task admin
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('task_name', 'project_id', 'assigned_to', 'status', 'due_date', 'completed')
    search_fields = ('task_name', 'description')
    list_filter = ('status', 'due_date', 'completed')
    ordering = ('-due_date',)

# Customize the Resource admin
@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'uploaded_at', 'featured')
    search_fields = ('title', 'description')
    list_filter = ('category', 'featured')
    ordering = ('-uploaded_at',)
