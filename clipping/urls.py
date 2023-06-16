from django.contrib import admin
from django.urls import path, include
from news_clippings_bot import urls as news_clippings_bot_urls

admin.autodiscover()
admin.site.enable_nav_sidebar = False

admin.site.site_header = 'Clipping Clipping Admin'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('news_clippings_bot/', include(news_clippings_bot_urls))
]
