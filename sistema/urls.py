from django.contrib import admin
from django.urls import path, include

from django.urls import re_path
from django.views import static as ds
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("core.urls")),
    re_path(r'^media/(?P<path>.*)$', ds.serve,
            {'document_root': settings.MEDIA_ROOT, }, name="media"),
]

# ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
