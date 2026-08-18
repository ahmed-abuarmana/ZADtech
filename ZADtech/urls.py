from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("core.urls")),
    path('articles/', include("articles.urls")),
    path('books/', include("books.urls")),
    path('courses/', include("courses.urls")),
    path('podcasts/', include("podcast.urls")),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
