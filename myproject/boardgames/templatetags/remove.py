
from django import template

register = template.Library()

@register.filter
def remove(value):
    value = value.replace(']', '')
    value = value.replace('[', '')
    value = value.replace('\'', '')
    value = value.replace(',', ', ')
    return value