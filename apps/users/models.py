from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager, Permission, _user_has_perm, _user_has_module_perms
from django.db import models

from model_utils.models import UUIDModel

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.update({'is_staff': True, 'is_superuser': True})
        return self._create_user(email, password, **extra_fields)

class Role(UUIDModel):
    name = models.CharField('Nombre', max_length=128)
    permissions = models.ManyToManyField(Permission)

    class Meta:
        verbose_name = 'Rol'
        verbose_name_plural = 'roles'
        ordering = ['name']

    def __str__(self):
        return self.name

# A custom model for users that inherits from AbstractUser
class User(UUIDModel, AbstractUser):
    email = models.EmailField('email', unique=True)
    role = models.ForeignKey(Role, models.SET_NULL, verbose_name='rol', null=True, blank=True)
    telegram_id = models.CharField('ID de Telegram', max_length=128, null=True, blank=True)
    objects = UserManager()

    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = 'usuario'
        verbose_name_plural = 'usuarios'
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

