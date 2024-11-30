from django import template

register = template.Library()

@register.filter
def in_list(value, list_string):
    return value in list_string.split(',')
