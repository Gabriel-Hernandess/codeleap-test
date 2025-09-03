from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('homepage.urls')),
    path('api/', include('careers.urls')),
    path('api/auth/', include('authenticate.urls')),
]