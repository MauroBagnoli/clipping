from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser, BaseUserManager, Permission, _user_has_perm, _user_has_module_perms
from django.db import models

from django.contrib.auth.models import PermissionsMixin 
from model_utils.models import UUIDModel

from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class UserManager(BaseUserManager):
    def create_user(self, email, date_of_birth, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, date_of_birth, password):
        """
        Creates and saves a superuser with the given email, and password.
        """
        user = self.create_user(email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


# A custom model for users that inherits from AbstractUser
class User(UUIDModel, AbstractUser, PermissionsMixin):
    email = models.EmailField(_('email'), unique=True)
    telegram_id = models.CharField(_('telegram ID'), max_length=128, null=True, blank=True)
    objects = UserManager()

    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural =  _('users')
        ordering = ['email']

    def __str__(self):
        return f'{self.display_name} ({self.email})'

    def save(self, *args, **kwargs):
        self.email = self.email.lower()
        return super().save(*args, **kwargs)

    @property
    def display_name(self):
        return ' '.join(filter(bool, [self.first_name, self.last_name])) or self.email

    def has_perm(self, perm, obj=None):
        # Always check with the auth backend.
        return _user_has_perm(self, perm, obj)

    def has_module_perms(self, app_label):
        # Always check with the auth backend.
        return _user_has_module_perms(self, app_label)
