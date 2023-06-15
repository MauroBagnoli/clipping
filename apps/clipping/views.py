
from .models import Article
from django.views.generic.list import ListView


class ArticleViewSet(ListView):
    model = Article
    paginate_by = 100
    search_fields = ['title']
    ordering_fields = ['name']
