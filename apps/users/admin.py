from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import user_passes_test

from .models import User, Role
from .forms import CreateUserAdminForm, RoleAdminForm
from django.contrib.auth.models import Group

# In admin.py
from django.contrib import admin
from django.contrib.auth.decorators import permission_required
from .models import User

admin.site.unregister(Group)


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = [
        'name__unaccent__icontains',
        'permissions__unaccent__icontains',
    ]
    form = RoleAdminForm

    def get_permission_count(self, obj):
        print('permission count: ', obj.permissions.count())
        return obj.permissions.count()

    get_permission_count.short_description = _('permission count')


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'last_name','role']
    readonly_fields = ['telegram_id']

    exclude=['groups']
    search_fields = [
        'email__unaccent__icontains',
        'first_name__unaccent__icontains',
        'last_name__unaccent__icontains',
    ]
    form = CreateUserAdminForm
    list_filter = ['role']
    # permissions = [ ('manage_users', _('Manage users')) ]

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj:
            print('form.base_fields: ', form.base_fields)
            form.base_fields.pop('password', None)
        return form
