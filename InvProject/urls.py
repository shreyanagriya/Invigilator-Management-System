from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from InvApp.views import handler404
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('InvApp.urls')),

]
handler404 = handler404
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
