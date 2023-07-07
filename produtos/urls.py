from django.urls import path
from . import views

urlpatterns = [
    path('cadastro_produtos/', views.cadastro_produtos, name='cadastro_produtos'),
    path('listar_produtos/', views.listar_produtos, name='listar_produtos'),
    path('editar_produto/<int:produto_id>/', views.editar_produto, name='editar_produto'),
    path('relatorio-geral/', views.gerar_relatorio_geral, name='relatorio_geral'),
    path('relatorio_perso/',views.relatorio_personalizado, name='relatorio_personalizado'),
    path('relatorio_compras_pdf/', views.relatorio_compras_pdf, name='relatorio_compras_pdf'),
    path('gerar_relatorio_geral/', views.gerar_relatorio_geral, name='gerar_relatorio_geral'),
   

]


    
    

