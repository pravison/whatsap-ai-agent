
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static




admin.site.site_header = 'SALESFLOW PRO'


urlpatterns = [
    path('', admin.site.urls),
    ]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
