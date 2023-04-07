from django.urls import path
from .views import get_file, get_file_2

urlpatterns = [
    path('ler/<str:arquivo>', get_file_2, name='get_file'),
   
    
    # path('config/<str:cols>', set_cols, name='set_cols')
    
]