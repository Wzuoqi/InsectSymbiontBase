from django import template
from django.contrib.staticfiles.storage import staticfiles_storage

register = template.Library()

@register.filter
def static_exists(path):
    """Check if a static file exists"""
    return staticfiles_storage.exists(path)