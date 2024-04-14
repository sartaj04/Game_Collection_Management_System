from django import template

register = template.Library()

@register.simple_tag
def profile_sections():
    return ['Basic Details', 'Library', 'Wishlist', 'Game Communities', 'Reviews', 'Clubs']
