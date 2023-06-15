from django.contrib import admin

from .models import Clipping, Tag

@admin.register(Clipping)
class ClippingAdmin(admin.ModelAdmin):
    list_display = ['title', 'date', 'source', 'author']
    search_fields = [
        'title__unaccent__icontains',
        'tags__unaccent__icontains',
        'source__unaccent__icontains',
        'author__unaccent__icontains',
    ]
    list_filter = ['author']

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = [
        'name__unaccent__icontains',
    ]
