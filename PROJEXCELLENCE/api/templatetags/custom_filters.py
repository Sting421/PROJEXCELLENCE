from django import template

register = template.Library()

@register.filter
def dict_get(d, key):
    return d.get(key)

@register.filter
def is_project_manager(user, project):
    return project.team_memberships.filter(user=user, role='Project Manager').exists()