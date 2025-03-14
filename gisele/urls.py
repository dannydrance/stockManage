from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from stoke.views import send_daily_report

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('stoke.urls')),
]

# Add this to serve static files in production (when DEBUG = False)
if not settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
