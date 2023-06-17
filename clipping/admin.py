from django.contrib import admin
from django.contrib.auth.models import Group

admin.site.unregister(Group)

class MyAdminSite(admin.AdminSite):
    site_header = "My custom title"
    site_title = "My custom site"
    index_title = "My custom index"

admin_site = MyAdminSite(name="myadmin")
