import django_filters
from django.forms.widgets import DateInput
from .models import User, Task

class TaskFilter(django_filters.FilterSet):
    due_date_range = django_filters.DateFromToRangeFilter(
        field_name="due_date",
        widget=django_filters.widgets.RangeWidget(attrs={"type": "date"}),
    )

    class Meta:
        model = Task
        fields = ["due_date_range"]
