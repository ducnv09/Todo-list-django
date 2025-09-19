from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),  # allauth URLs (bao gồm Google OAuth)
    path("auth/", include("django.contrib.auth.urls")),  # Django auth URLs
    path("api/", include("tasks.api_urls")),  # API endpoints
    path("", include("tasks.urls")),  # Web routes của tasks
]
