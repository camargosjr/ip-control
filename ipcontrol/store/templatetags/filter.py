from django import template

register = template.Library()

@register.filter(name='is_par')
def is_par(value):
    if value % 2 == 0:
        return True
    
    return False

@register.filter
def get_value(dict, key):
    return dict.get(key)