from django.urls import path
from .views import get_file

urlpatterns = [
    path('ler/<str:arquivo>', get_file, name='get_file')
    
]