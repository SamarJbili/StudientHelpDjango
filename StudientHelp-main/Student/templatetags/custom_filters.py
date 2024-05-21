from django import template # type: ignore

register = template.Library()

@register.filter(name='instanceof')
def isinstanceof(obj, class_name):
    return obj.__class__.__name__ == class_name
