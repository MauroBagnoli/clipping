
from .models import Clipping
from django.views.generic.list import ListView


class ArticleViewSet(ListView):
    model = Clipping
    paginate_by = 100
    search_fields = ['title']
    ordering_fields = ['name']
