from django.urls import path
from .views import get_file, get_file_2, del_file

urlpatterns = [
    path('ler/<str:arquivo>', get_file_2, name='get_file'),
    path('tabela/<str:arquivo>', get_file, name='get_tabela'),
     path('deletar/<int:id>', del_file, name='del_file'),
    
   
    
    # path('config/<str:cols>', set_cols, name='set_cols')
    
]