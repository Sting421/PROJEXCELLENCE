import django_filters
from django.forms.widgets import DateInput
from .models import User, Task, Project, Team

class TaskFilter(django_filters.FilterSet):
    due_date_range = django_filters.DateFromToRangeFilter(
        field_name="due_date",
        widget=django_filters.widgets.RangeWidget(attrs={"type": "date"}),
    )

    class Meta:
        model = Task
        fields = ["due_date_range"]

class ProjectFilter(django_filters.FilterSet):
    date_created_range = django_filters.DateFromToRangeFilter(
        field_name="date_created",
        widget=django_filters.widgets.RangeWidget(attrs={"type": "date"}),
        label="Creation Date (Range)"
    )
    project_name = django_filters.CharFilter(
        field_name="project_name", lookup_expr="icontains", label="Project Name"
    )
    description = django_filters.CharFilter(
        field_name="description", lookup_expr="icontains", label="Description"
    )

    class Meta:
        model = Project
        fields = ["project_name", "description", "date_created_range"]

class TeamFilter(django_filters.FilterSet):
    team_name = django_filters.CharFilter(lookup_expr='icontains')
    users = django_filters.ModelMultipleChoiceFilter(queryset=User.objects.all())
    project = django_filters.ModelChoiceFilter(queryset=Project.objects.all())

    class Meta:
        model = Team
        fields = ['team_name', 'users', 'project']   