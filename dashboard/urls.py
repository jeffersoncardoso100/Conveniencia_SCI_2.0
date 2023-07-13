from django.urls import path
from . import views

urlpatterns = [
    # ... outras URLs do seu projeto ...

    path('', views.home, name='index'),  # Rota para a URL base vazia

    path('home/', views.home, name='home'),
    path('controle_estoque/', views.controle_estoque, name='controle_estoque'),
   

    # ... outras URLs do seu projeto ...
]
