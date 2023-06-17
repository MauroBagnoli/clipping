from django import forms
from django.conf import settings
from django.db.models import Q
from django.contrib import admin
from django.contrib.auth.models import Permission
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserChangeForm

from django.forms import widgets
from django.contrib.auth import authenticate, password_validation
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.hashers import make_password

from .models import User, Role


class RoleAdminForm(forms.ModelForm):
    custom_permissions = forms.ModelMultipleChoiceField(
        Permission.objects.none(),
        widget=admin.widgets.FilteredSelectMultiple(_('Custom permissions'), False),
        label=_('Custom permissions'),
        required=False,
    )

    django_permissions = forms.ModelMultipleChoiceField(
        Permission.objects.none(),
        widget=admin.widgets.FilteredSelectMultiple(_('Django permissions'), False),
        label=_('Django permissions'),
        required=False,
    )

    # We need to declare this field so the model form actually saves the m2m.
    permissions = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Role
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        custom_codenames = [p[0] for p in getattr(settings, 'CUSTOM_PERMISSIONS', [])]

        print('custom_codenames: ', custom_codenames)

        if kwargs.get('instance'):
            print('kwargs[instance].permissions: ', kwargs['instance'].permissions)
            kwargs['initial'] = {
                'custom_permissions': kwargs['instance'].permissions.filter(codename__in=custom_codenames),
                'django_permissions': kwargs['instance'].permissions.exclude(Q(codename__in=custom_codenames))
            }

        super().__init__(*args, **kwargs)

        print('self.fields[custom_permissions]: ', self.fields['custom_permissions'])

        self.fields['custom_permissions'].queryset = Permission.objects.filter(codename__in=custom_codenames)
        self.fields['django_permissions'].queryset = Permission.objects.exclude(Q(codename__in=custom_codenames))

    def clean(self):
        cleaned_data = super().clean()

        custom_permissions = cleaned_data.get('custom_permissions')
        django_permissions = cleaned_data.get('django_permissions')
        permission_ids = []

        print('custom_permissions: ', custom_permissions)

        if custom_permissions:
            permission_ids += custom_permissions.values_list('id', flat=True)

        if django_permissions:
            permission_ids += django_permissions.values_list('id', flat=True)

        print('permission_ids: ', permission_ids)

        cleaned_data['permissions'] = Permission.objects.filter(id__in=permission_ids)

        return cleaned_data


class AuthenticationForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField()


    error_messages = {
        'inactive': _('This user is inactive.'),
        'invalid_login': _('Please enter a correct email and password.'),
    }

    def __init__(self, request=None, *args, **kwargs):
        print('starting auth process')

        self.request = request
        self.user = None
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        print('email: ', email)

        invalid_login = forms.ValidationError(self.error_messages['invalid_login'], code='invalid_login')

        print('invalid_login: ', invalid_login)

        if email and password:
            try:
                user = User.objects.get(email__iexact=email)
            except User.DoesNotExist:
                try:
                    user = User.objects.get(email__iexact=email)
                except User.DoesNotExist:
                    raise invalid_login

            if not user.is_active:
                raise forms.ValidationError(self.error_messages['inactive'], code='inactive')

            print('before authenticate')
            self.user = authenticate(self.request, username=user.email, password=password)
            if self.user is None:
                raise invalid_login

        return cleaned_data


class BaseResetPasswordForm(forms.Form):
    email = forms.EmailField()

    error_messages = {
        'not_found': _('There is no registered user with that email.'),
        'inactive': _('This user is inactive.'),
        'duplicate_email': _('More than one user with same email.'),
    }

    job = None

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user = None
        super().__init__(*args, **kwargs)

    def clean(self):
        email = self.cleaned_data.get('email')
        user = User.objects.filter(email__iexact=email)

        if not user.exists():
            raise forms.ValidationError(self.error_messages['not_found'], code='not_found')
        
        if user.count() > 1:
            raise forms.ValidationError(self.error_messages['duplicate_email'], code='duplicate_email')

        self.user = user.get()
        if not self.user.is_active:
            raise forms.ValidationError(self.error_messages['inactive'], code='inactive')

        return email

    def save(self):
        self.job.delay(self.user.id)

class SetPasswordForm(forms.Form):
    user = forms.UUIDField()
    token = forms.CharField()
    password = forms.CharField()

    error_messages = {
        'invalid_link': _('Link is invalid or expired, please restart the process and try again.'),
    }

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user = None
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        if not password:
            return cleaned_data

        user = cleaned_data.get('user')
        token = cleaned_data.get('token')

        try:
            self.user = User.objects.get(id=user)
        except Exception:
            raise forms.ValidationError(self.error_messages['invalid_link'], code='invalid_link')

        if not default_token_generator.check_token(self.user, token):
            raise forms.ValidationError(self.error_messages['invalid_link'], code='invalid_link')

        try:
            password_validation.validate_password(password, self.user)
        except forms.ValidationError as error:
            raise forms.ValidationError(error, code='validation_error')

        return cleaned_data

    def save(self, commit=True):
        self.user.set_password(self.cleaned_data['password'])
        if commit:
            self.user.save()
        return self.user


class UpdatePasswordForm(forms.Form):
    new_password = forms.CharField()
    current_password = forms.CharField()

    def __init__(self, user=None, request=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
        self.user = user

    def clean_current_password(self):
        current_password = self.cleaned_data.get('current_password')
        if not self.user.check_password(current_password):
            raise forms.ValidationError(_('Current password is incorrect.'), code='incorrect_current_password')
        return current_password

    def clean_new_password(self):
        new_password = self.cleaned_data.get('new_password')
        password_validation.validate_password(new_password, self.user)
        return new_password

    def save(self, commit=True):
        self.user.set_password(self.cleaned_data['new_password'])
        if commit:
            self.user.save()
        return self.user


class UserAdminForm(forms.ModelForm):
    class Meta:
        model = User
        exclude = ['last_login']


class CreateUserAdminForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name', 'role']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

    def save(self, commit=True):
        user = super().save(commit=False)
        print('self.fields: ', self.fields)
        if not user.password:
            print('self.fields[password] ', self.fields['password'])
            password = self.cleaned_data['password']
            user.password = make_password(password)
        user.is_staff = True

        if commit:
            user.save()
        return user
