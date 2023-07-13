from datetime import date
from itertools import count
from operator import countOf
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from collections import Counter
from requests import request
from estoque.models import Estoque
from produtos.models import Produto
from registro_de_compras.models import Compra, ItemCompra
from django.db.models import Sum
from produtos.models import Produto


@login_required(login_url='login')
def home(request):
    return controle_estoque(request)


def controle_estoque(request):
    produtos_estoque = Estoque.objects.filter(produto__situacao='Ativo')
    lista_estoque = []

    for produto_estoque in produtos_estoque:
        quantidade = produto_estoque.quantidade

        if quantidade >= 10:
            cor_card = 'verde'
        elif quantidade <= 6:
            cor_card = 'amarelo'
        elif quantidade <= 3:
            cor_card = 'vermelho'
        else:
            cor_card = 'padrao'

        lista_estoque.append({
            'produto': produto_estoque.produto.nome,
            'quantidade': quantidade,
            'cor_card': cor_card
        })

    # Obter os 3 produtos mais vendidos
    produtos_mais_vendidos = obter_produtos_mais_vendidos()

    # Obter os produtos vendidos hoje
    produtos_vendidos_hoje = obter_produtos_vendidos_hoje()

    context = {
        'produtos_estoque': lista_estoque,
        'produtos_mais_vendidos': produtos_mais_vendidos,
        'produtos_vendidos_hoje': produtos_vendidos_hoje
    }

    return render(request, 'home.html', context)

def obter_produtos_mais_vendidos():
    produtos_mais_vendidos = ItemCompra.objects.values('produto').annotate(
        quantidade_vendida=Sum('quantidade')).order_by('-quantidade_vendida')[:3]

    # Mapear os IDs dos produtos mais vendidos para seus respectivos objetos de Produto
    produtos_mais_vendidos = [Produto.objects.get(
        pk=produto['produto']) for produto in produtos_mais_vendidos]

    return produtos_mais_vendidos


from datetime import datetime, date



def obter_produtos_vendidos_hoje():
    data_atual = datetime.now().date()
    compras_hoje = Compra.objects.filter(data_compra__year=data_atual.year, data_compra__month=data_atual.month, data_compra__day=data_atual.day)
    ids_compras_hoje = compras_hoje.values_list('id', flat=True)
    itens_vendidos_hoje = ItemCompra.objects.filter(compra_id__in=ids_compras_hoje)
    produtos_vendidos_hoje = [(item.produto.nome, item.quantidade) for item in itens_vendidos_hoje]
    return produtos_vendidos_hoje
