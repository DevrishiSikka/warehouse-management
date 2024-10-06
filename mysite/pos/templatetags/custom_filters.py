from django import template

register = template.Library()

@register.filter
def multiply(value1, value2):
    try:
        return float(value1) * float(value2)
    except (ValueError, TypeError):
        return 0  # Return 0 if there's an error
