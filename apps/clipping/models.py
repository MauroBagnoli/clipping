from django.db import models
from apps.users.models import User
from django.utils.translation import gettext_lazy as _

class Tag(models.Model):
    name = models.CharField(_('Name'), max_length=100)

    class Meta:
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')
        ordering = ['name']

    def __str__(self):
        return self.name


class Clipping(models.Model):
    title = models.CharField(_('Title'), max_length=200, null=True, blank=True)
    published_on = models.DateTimeField(_('Published on'), null=True, blank=True)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name=_('Created by'), null=True, blank=True)
    tags = models.ManyToManyField(Tag, verbose_name=_('tags'), related_name='articles', null=True, blank=True)
    url = models.URLField('URL', unique=True, error_messages=_('This url has already been uploaded.'))
    author = models.CharField(_('Author'), max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = _('Article')
        verbose_name_plural = _('Articles')
        ordering = ['created_at', 'title']

    def __str__(self):
        return self.url
