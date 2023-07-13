
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.shortcuts import render
from produtos.models import Produto
from .models import Estoque, MovimentacaoEstoque
from django.contrib.auth.decorators import login_required, user_passes_test





@login_required(login_url='login')
def estoque(request):
    lista_estoque=[]
    produtos = Produto.objects.all()
    for item in produtos: 
        if item.situacao == 'Ativo':
            produtos_estoque = Estoque.objects.get(produto=item.id)
            lista_estoque.append({'produto':produtos_estoque.produto,'quantidade':produtos_estoque.quantidade})
    return render(request, 'estoque.html', {'produtos_estoque':lista_estoque})


@login_required(login_url='login')
def aumentar_estoque(request, produto_id):
    if request.method == 'POST':
        try:
            novo_valor = int(request.POST.get('novaQuantidade'))
            estoque = get_object_or_404(Estoque, produto_id=produto_id)

        
            estoque_atualizado= int(estoque.quantidade) +  int(novo_valor)
            estoque.quantidade = estoque_atualizado
            estoque.save()

            # Obtém o usuário responsável pela alteração de estoque
            usuario = request.user

            # Registra a movimentação de estoque
            produto=Produto.objects.get(id=produto_id)
            movimentacao = MovimentacaoEstoque(
                tipo_movimentacao='entrada',
                quantidade=novo_valor,
                usuario=usuario,
                produto=produto
            )
            movimentacao.save()

            return HttpResponse("Estoque atualizado com sucesso!")
        
            

        except Estoque.DoesNotExist:
            return HttpResponse("Produto não encontrado no estoque.")
    else:
        return HttpResponse("Método de requisição inválido.")


@login_required(login_url='login')
def diminuir_estoque(request, produto_id):
    if request.method == 'POST':
        try:
            novo_valor = int(request.POST.get('novaQuantidade'))
            estoque = get_object_or_404(Estoque, produto_id=produto_id)

            if novo_valor <= estoque.quantidade:
                estoque.quantidade -= novo_valor  # Diminuir a quantidade corretamente
                estoque.save()

                # Obtém o usuário responsável pela alteração de estoque
                usuario = request.user

                # Registra a movimentação de estoque
                produto = Produto.objects.get(id=produto_id)
                movimentacao = MovimentacaoEstoque(
                    tipo_movimentacao='baixa',
                    quantidade=novo_valor,
                    usuario=usuario,
                    produto=produto
                )
                movimentacao.save()

                return HttpResponse("Estoque atualizado com sucesso!")
            else:
                return HttpResponse("A nova quantidade deve ser menor ou igual ao estoque atual.")

        except Estoque.DoesNotExist:
            return HttpResponse("Produto não encontrado no estoque.")
    else:
        return HttpResponse("Método de requisição inválido.")



@login_required(login_url='login')
def movimentacao_estoque(request):
    movimentacoes_entrada = MovimentacaoEstoque.objects.filter(tipo_movimentacao='entrada')
    movimentacoes_baixa = MovimentacaoEstoque.objects.filter(tipo_movimentacao='baixa')
    movimentacoes = list(movimentacoes_entrada) + list(movimentacoes_baixa)
    return render(request, 'movimentacao_estoque.html', {'movimentacoes': movimentacoes})
