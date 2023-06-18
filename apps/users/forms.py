from django import forms
from .models import User


class UserAdminForm(forms.ModelForm):
    class Meta:
        model = User
        exclude = ['last_login']
