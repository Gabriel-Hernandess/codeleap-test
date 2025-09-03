from django.urls import path
from .views import CareersView

urlpatterns = [
    path('careers/', CareersView.as_view(), name='careers'),                           # GET, POST (careers)
    path('careers/<int:id>/', CareersView.as_view(), name='careers-detail'),           # PATCH, DELETE (careers)

    
]