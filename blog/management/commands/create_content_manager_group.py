from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from blog.models import BlogPost

class Command(BaseCommand):
    help = 'Create content manager group and assign permissions'

    def handle(self, *args, **kwargs):
        # Создание группы
        content_manager_group, created = Group.objects.get_or_create(name='Контент-менеджер')

        # Получение прав
        content_type = ContentType.objects.get_for_model(BlogPost)
        can_add_blogpost = Permission.objects.get(codename='add_blogpost', content_type=content_type)
        can_change_blogpost = Permission.objects.get(codename='change_blogpost', content_type=content_type)
        can_delete_blogpost = Permission.objects.get(codename='delete_blogpost', content_type=content_type)

        # Назначение прав группе
        content_manager_group.permissions.add(can_add_blogpost, can_change_blogpost, can_delete_blogpost)

        self.stdout.write(self.style.SUCCESS('Successfully created content manager group and assigned permissions'))