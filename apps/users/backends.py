from django.conf import settings
from django.contrib.auth.backends import ModelBackend as BaseModelBackend, UserModel
from django.contrib.auth.models import Permission
from django.db.models import Q

from apps.users.models import User


class ModelBackend(BaseModelBackend):
    """
    Extend the default ModelBackend to support user roles and custom permissions.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)

        if username is None or password is None:
            return
        user = UserModel._default_manager.get_by_natural_key(username)

        if user.check_password(password) and self.user_can_authenticate(user):
            return user

    def _get_user_permissions(self, user_obj):
        """
        Custom permissions must always be assigned explicitly.
        """

        if user_obj.is_superuser:
            custom_codenames = [p[0] for p in getattr(settings, 'CUSTOM_PERMISSIONS', [])]
            return Permission.objects.filter(
                Q(id__in=user_obj.user_permissions.values_list('id', flat=True))
                | ~Q(codename__in=custom_codenames)
            )

        return user_obj.user_permissions.all()

    def _get_group_permissions(self, user_obj):
        """
        User role overrides the default groups implementation.
        """

        if not user_obj.role:
            return Permission.objects.none()

        return user_obj.role.permissions.all()

    def _get_permissions(self, user_obj, obj, from_name):
        if not user_obj.is_active or user_obj.is_anonymous or obj is not None:
            return set()

        perm_cache_name = '_%s_perm_cache' % from_name
        if not hasattr(user_obj, perm_cache_name):
            perms = getattr(self, '_get_%s_permissions' % from_name)(user_obj)
            perms = perms.values_list('content_type__app_label', 'codename').order_by()
            setattr(user_obj, perm_cache_name, {"%s.%s" % (ct, name) for ct, name in perms})
        return getattr(user_obj, perm_cache_name)
