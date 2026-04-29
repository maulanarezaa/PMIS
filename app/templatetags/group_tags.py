from django import template
from django.http import HttpResponseForbidden
from django.shortcuts import render

register = template.Library()

@register.filter
def has_any_group(user, group_names):
    group_list = [g.strip() for g in group_names.split(',')]
    return user.groups.filter(name__in=group_list).exists()
@register.filter
def group_required(*group_names):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if request.user.groups.filter(name__in=group_names).exists():
                return view_func(request, *args, **kwargs)
            return render(request, 'Login/error-403.html', status=403)
        return wrapper
    return decorator