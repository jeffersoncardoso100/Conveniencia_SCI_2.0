from django.urls import path
from . import views

urlpatterns = [
    # Outras URLs do seu aplicativo...

    # URL para o relatório de consumo detalhado dos produtos por colaborador
    path('relatorio_compras_pdf/', views.RelatorioComprasPDFView, name='relatorio_compras_pdf'),

    # URL para o relatório de total consumido por todos os colaboradores na referência atual
]
