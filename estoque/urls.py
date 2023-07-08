from os import path


from django.urls import path

from estoque import views
from .views import estoque

urlpatterns = [
    # Other URL patterns
    path('estoque/', estoque, name='estoque'),
    path('estoque/alterar/<int:produto_id>/', views.alterar_estoque, name='alterar_estoque'),
    path('controle_estoque/', views.controle_estoque, name='controle_estoque'),
]
