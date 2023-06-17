from django.contrib import admin

from .models import User, Role
from .forms import UserAdminForm, RoleAdminForm

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = [
        'name__unaccent__icontains',
        'permissions__unaccent__icontains',
    ]
    form = RoleAdminForm

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'last_name','role']
    exclude=['groups']
    search_fields = [
        'email__unaccent__icontains',
        'first_name__unaccent__icontains',
        'last_name__unaccent__icontains',
    ]
    form = UserAdminForm
    list_filter = ['role']
