from django.contrib import admin

from .models import User
from .forms import UserAdminForm

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'last_name','role']
    search_fields = [
        'email__unaccent__icontains',
        'first_name__unaccent__icontains',
        'last_name__unaccent__icontains',
    ]
    form = UserAdminForm
    list_filter = ['role']
