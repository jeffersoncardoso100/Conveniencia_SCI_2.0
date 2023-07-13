from os import path


from django.urls import path

from estoque import views
from .views import estoque

urlpatterns = [
    # Other URL patterns
    path('estoque/', estoque, name='estoque'),
    path('estoque/aumentar/<int:produto_id>/', views.aumentar_estoque, name='aumentar_estoque'),
    path('estoque/diminuir/<int:produto_id>/', views. diminuir_estoque, name='alterar_estoque'),
    path('movimentacao-estoque/', views.movimentacao_estoque, name='movimentacao_estoque'),
]
