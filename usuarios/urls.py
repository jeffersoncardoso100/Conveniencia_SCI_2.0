from django.urls import path

from colaboradores.views import criar_colaboradores
from . import views

urlpatterns = [
    # ... outras URLs do seu projeto ...
    path('', views.login_usuario, name='login'),
    
    path('logout/', views.logout_view, name='logout'),
    path('cadastrar_usuario/', views.cadastrar_usuario, name='cadastrar_usuario'),
    path('listar_usuario/', views.listar_usuarios, name='listar_usuarios'),
    path('deletar_usuario/<int:user_id>/', views.deletar_usuario, name='deletar_usuario'),
    path('editar_usuario/<int:user_id>/', views.editar_usuario, name='editar_usuario'),
    
    ]