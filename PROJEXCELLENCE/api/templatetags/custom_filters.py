from django import template
from ..models import TeamMembership

register = template.Library()

@register.filter
def dict_get(d, key):
    return d.get(key)

@register.filter
def is_project_manager(user, project):
   
    return TeamMembership.objects.filter(
        user=user,
        project=project,
        role='Project Manager'
    ).exists()

@register.filter
def get_item(dictionary, key):
    """Get an item from a dictionary using bracket notation"""
    return dictionary.get(key)

@register.filter
def multiply(value, arg):
    return value * arg