"""Project URL configuration for AI-Solution."""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

admin.site.index_template = "admin/ai_analytics_index.html"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("website.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
