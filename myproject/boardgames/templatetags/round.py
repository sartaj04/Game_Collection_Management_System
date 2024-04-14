
from django import template

register = template.Library()

@register.filter
def round(value):
    return str(value)[0:4]