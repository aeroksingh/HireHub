from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),

    path("", include("apps.jobs.urls")),
    path("", include("apps.accounts.urls")),
    # path("", include("apps.applications.urls")),
    path("applications/", include("apps.applications.urls")),
    path("recruiter/", include("apps.recruiter.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
