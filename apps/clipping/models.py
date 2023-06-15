from django.db import models

class Clipping(models.Model):
    title = models.CharField('Título', max_length=200)
    date = models.DateField('Fecha')
    tags = models.ManyToManyField('Tag', verbose_name='tags', related_name='articles')
    source = models.URLField('Fuente')
    author = models.CharField('Autor', max_length=100)
    content = models.TextField('Contenido')

    class Meta:
        verbose_name = 'Artículo'
        verbose_name_plural = 'Artículos'
        ordering = ['date', 'title']

    def __str__(self):
        return self.title

class Tag(models.Model):
    name = models.CharField('Nombre', max_length=100)

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
        ordering = ['name']

    def __str__(self):
        return self.name
