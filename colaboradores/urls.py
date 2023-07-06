from django.urls import path

from django import views
from .views import criar_colaboradores
from colaboradores import views



urlpatterns = [
   
    path('criar_colaboradores/', views.criar_colaboradores, name='criar_colaboradores'),
    path('listar_colaboradores/', views.listar_colaboradores, name='listar_colaboradores'),
    path('editar_colaborador/<int:colaborador_id>/', views.editar_colaborador, name='editar_colaborador'),
    path('visualizar_colaborador/<int:colaborador_id>/', views.visualizar_colaborador, name='visualizar_colaborador'),

]
