from django import template
import re

register = template.Library()

@register.filter
def wishList(value):
    if(value != "Not Available"):
        pattern = r'\'(.*?)\''
        matches = re.findall(pattern, value)
    
    else:
        matches = "No"

    return matches
