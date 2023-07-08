from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render
from produtos.models import Produto
from .models import Estoque

def estoque(request):
    lista_estoque=[]
    produtos = Produto.objects.all()
    for item in produtos: 
        if item.situacao == 'Ativo':
            produtos_estoque = Estoque.objects.get(produto=item.id)
            lista_estoque.append({'produto':produtos_estoque.produto,'quantidade':produtos_estoque.quantidade})
    return render(request, 'estoque.html', {'produtos_estoque':lista_estoque})


def alterar_estoque(request, produto_id):
    if request.method == 'POST':
        try:
            novo_valor = int(request.POST.get('novaQuantidade'))
            estoque = Estoque.objects.get(produto=produto_id)
            estoque.quantidade = novo_valor
            estoque.save()
            return HttpResponse("Estoque atualizado com sucesso!")
        except Estoque.DoesNotExist:
            return HttpResponse("Produto não encontrado no estoque.")
    else:
        return HttpResponse("Método de requisição inválido.")
    

def controle_estoque(request):
    lista_estoque = []
    produtos = Produto.objects.all()
    
    for item in produtos: 
        if item.situacao == 'Ativo':
            produtos_estoque = Estoque.objects.get(produto=item.id)
            if produtos_estoque.quantidade >= 3:
                lista_estoque.append({'produto': produtos_estoque.produto, 'quantidade': produtos_estoque.quantidade})
    
    return render(request, 'controle.html', {'produtos_estoque': lista_estoque})
