# myapp/templatetags/custom_filters.py

from django import template

register = template.Library()

@register.filter(name='truncate_after_comma')
def truncate_after_comma(value):
    """
    Removes all characters after the first comma in the given string.
    """

    if isinstance(value, str):
        return value.split(',')[0]
    return value
