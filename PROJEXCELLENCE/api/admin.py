from django.contrib import admin

# Register your models here.
from .models import Team, Project, Task

admin.site.register(Team)
admin.site.register(Project)
admin.site.register(Task)
