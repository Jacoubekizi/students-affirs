from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from client.admin import post_admin_site

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin_site/', post_admin_site.urls),
    path('api/', include('client.urls')),
]+ static(settings.MEDIA_URL , document_root=settings.MEDIA_ROOT)
