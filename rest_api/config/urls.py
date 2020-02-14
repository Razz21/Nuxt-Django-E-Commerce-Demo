from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static


# todo api-root-url

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("project.users.urls")),
    path("api/", include("project.core.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    from django.conf.urls.static import static

    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
