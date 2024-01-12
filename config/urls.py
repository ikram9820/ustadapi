
from django.contrib import admin
from django.urls import path , include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('services.urls')),
    path('api/chat/',include('chat.urls')),
    path('api/auth/',include('djoser.urls')),
    path('api/auth/', include('djoser.urls.jwt')),
    path('__debug__/', include('debug_toolbar.urls')),
]
