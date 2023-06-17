from django.conf import settings
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from ...models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING('Creating custom permissions:'))

        custom_permissions = getattr(settings, 'CUSTOM_PERMISSIONS', [])
        user_content_type = ContentType.objects.get_for_model(User)

        # Update or create active custom permissions.
        for codename, name in custom_permissions:
            self.stdout.write(f'  Creating {codename}...', ending='')
            Permission.objects.update_or_create(
                codename=codename,
                content_type=user_content_type,
                defaults={'name': name},
            )
            self.stdout.write(self.style.SUCCESS(' OK'))

        # Delete old custom permissions.
        # This might break if django changes default permission codenames.
        old_permissions = Permission.objects \
            .filter(content_type=user_content_type) \
            .exclude(codename__in=['add_user', 'change_user', 'delete_user', 'view_user']) \
            .exclude(codename__in=[codename for codename, _ in custom_permissions]) \

        if old_permissions:
            for old_permission in old_permissions:
                self.stdout.write(f'  Deleting {old_permission.codename}...', ending='')
                old_permission.delete()
                self.stdout.write(self.style.SUCCESS(' OK'))
