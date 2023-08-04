from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.views import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('virtual_app.urls')),
    path('accounts/', include('accounts.urls')),
]

# Serve static files in production using Django's static() function
if settings.DEBUG:
    # In development, serve static files through Django for simplicity
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
else:
    # In production, configure your web server to serve static files
    # and media files. The urlpatterns here are for media files.
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    ]
