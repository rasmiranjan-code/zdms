from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    if dictionary:
        return dictionary.get(key)
    return None

@register.filter(name='replace')
def replace_str(value, arg):
    """
    Replaces all occurrences of the first part of the arg with the second.
    Usage: {{ "CREATED_STUDENT_ACCOUNT"|replace:"_," }}
    """
    if isinstance(value, str) and isinstance(arg, str) and ',' in arg:
        old, new = arg.split(',', 1)
        return value.replace(old, new)
    return value