
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('app/', include('app.urls')),
    path('customer/', include('customer.urls')),
    ]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
