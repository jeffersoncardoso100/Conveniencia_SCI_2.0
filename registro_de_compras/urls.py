from django.urls import path
from . import views


urlpatterns = [
    path('cadastrar-compra/', views.CadastrarCompra, name='cadastrar_compra'),
    path('finalizar-compra/', views.FinalizarCompra, name='finalizar_compra'),
    path('listar-compra/', views. ListarCompra, name='listar_compra'),
    path('limpar-carrinho/', views.LimparCarrinho, name='limpar_carrinho'),
    path('excluir-item/<int:item_id>/', views.ExcluirItem, name='excluir_item'),
    path('valor_referencia_anterior/', views.ValorReferenciaAnterior, name='valor_referencia_anterior'),
    path('valor_referencia_atual/', views.ValorReferenciaAtual, name='valor_referencia_atual'),
    path('visualizar_gastos/', views.VisualizarGastos, name='visualizar_gastos'),
    path('enviar_email/', views.enviar_email, name='enviar_email'),
  
  
   
]

    
  




   
   