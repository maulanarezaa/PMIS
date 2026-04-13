from django import template

register = template.Library()

@register.filter
def has_any_group(user, group_names):
    group_list = [g.strip() for g in group_names.split(',')]
    return user.groups.filter(name__in=group_list).exists()