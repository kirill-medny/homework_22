from django import template
from django.contrib.auth.models import Group

register = template.Library()

@register.filter()
def media_filter(path):
    if path:
        return f"/media/{path}"
    return "#"

@register.filter(name='has_group')
def has_group(user, group_name):
    """
    Проверяет, является ли пользователь членом указанной группы.
    """
    try:
        group = Group.objects.get(name=group_name)
    except Group.DoesNotExist:
        return False  # Группа не существует
    return group in user.groups.all()

@register.filter(name='in_any_group')
def in_any_group(user, group_names):
    """
    Проверяет, является ли пользователь членом хотя бы одной из указанных групп.
    group_names - строка, содержащая имена групп, разделенные запятыми.
    """
    group_list = [s.strip() for s in group_names.split(",")]
    for group_name in group_list:
        try:
            group = Group.objects.get(name=group_name)
            if group in user.groups.all():
                return True
        except Group.DoesNotExist:
            pass  # Игнорируем несуществующие группы
    return False