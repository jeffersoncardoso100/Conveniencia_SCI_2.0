from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from email.message import EmailMessage
import smtplib
from django.shortcuts import render
from django.db.models import Sum
import datetime
from gettext import translation
from django.shortcuts import render, redirect
from django.contrib import messages
from django.test import TransactionTestCase

from Conveniencia_SCI_2_0 import settings
from estoque.models import Estoque
from .models import Compra, ItemCompra, Produto, Colaborador
from django.db.models import F
from django.db import transaction
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required


def CadastrarCompra(request):
    if request.method == 'POST':
        codigo_barras = request.POST.get('codigo_barras')

        if Produto.objects.filter(codigo_barras=codigo_barras).exists():
            try:
                produto = Produto.objects.get(codigo_barras=codigo_barras)

                if produto.situacao == 'Ativo':
                    # Adicionar o produto ao carrinho em sessão
                    carrinho = request.session.get('carrinho', [])
                    carrinho.append(produto.id)
                    request.session['carrinho'] = carrinho

                    messages.success(
                        request, 'Produto adicionado ao carrinho!')
                else:
                    messages.warning(
                        request, 'Produto inativado. Não é possível adicioná-lo.')
            except Produto.DoesNotExist:
                messages.error(
                    request, 'Produto com código de barras inválido.')
        else:
            messages.error(request, 'Produto com código de barras inválido.')

    carrinho_ids = request.session.get('carrinho', [])
    carrinho = []
    for produto_id in carrinho_ids:
        produto = Produto.objects.get(id=produto_id)
        carrinho.append(produto)
    valor_total = sum(produto.preco_produto for produto in carrinho)
    colaboradores = Colaborador.objects.all()

    # Verificar se há mensagem de erro de produto inativo
    produto_inativo_message = None
    for message in messages.get_messages(request):
        if message.level_tag == 'warning' and message.message == 'Produto inativado. Não é possível adicioná-lo ao carrinho.':
            produto_inativo_message = message
            break

    
    return render(request, 'registro.html', {'carrinho': carrinho, 'valor_total': valor_total, 'colaboradores': colaboradores, 'produto_inativo_message': produto_inativo_message})
"""
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
import base64


#função sem pdf

def enviar_email(destinatario, assunto, mensagem, produtos, data_hora_compra, nome_colaborador):
    email_servidor = settings.EMAIL_HOST_USER

    # Calcular o valor total da compra
    valor_total = sum(produto.preco_produto for produto in produtos)

    # Renderizar o template com as variáveis
    context = {
        'produtos': produtos,
        'valor_total': valor_total,
        'data_hora_compra': data_hora_compra,
        'nome_colaborador': nome_colaborador
    }
    mensagem_html = render_to_string('email_template.html', context)

    # Criar uma instância de EmailMultiAlternatives
    email_message = EmailMultiAlternatives()
    email_message.subject = assunto
    email_message.from_email = email_servidor
    email_message.to = [destinatario]
    email_message.body = mensagem

    # Adicionar o conteúdo HTML como uma alternativa ao corpo do email
    email_message.attach_alternative(mensagem_html, 'text/html')

    email_message.send()"""

#função com pdf

from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from weasyprint import HTML

def enviar_email(destinatario, assunto, mensagem, produtos, data_hora_compra, nome_colaborador):
    email_servidor = settings.EMAIL_HOST_USER

    # Calcular o valor total da compra
    valor_total = sum(produto.preco_produto for produto in produtos)

    # Renderizar o template com as variáveis
    context = {
        'produtos': produtos,
        'valor_total': valor_total,
        'data_hora_compra': data_hora_compra,
        'nome_colaborador': nome_colaborador
    }
    mensagem_html = render_to_string('email_template.html', context)

    # Converter o conteúdo HTML em PDF usando o weasyprint
    pdf_bytes = HTML(string=mensagem_html).write_pdf()

    # Criar uma instância de EmailMessage
    email_message = EmailMessage()
    email_message.subject = assunto
    email_message.from_email = email_servidor
    email_message.to = [destinatario]
    email_message.body = mensagem

    # Anexar o PDF ao email
    email_message.attach(f'comprovante_{data_hora_compra}.pdf', pdf_bytes, 'application/pdf')

    email_message.send()
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction
import datetime

def FinalizarCompra(request):
    if request.method == 'POST':
        carrinho_ids = request.session.get('carrinho', [])
        login = request.POST.get('login')
        senha = request.POST.get('senha')

        # Verifique as credenciais do colaborador
        colaborador = None
        try:
            colaborador = Colaborador.objects.get(login=login)

            if not check_password(senha, colaborador.senha):
                raise Colaborador.DoesNotExist
        except Exception as e:
            if 'Colaborador' in str(e):
                messages.error(request, 'Credenciais inválidas')
            return redirect('cadastrar_compra')

        # Verifique a situação do colaborador apenas se o objeto colaborador for encontrado
        if colaborador.situacao == 'Inativo':
            messages.error(request, 'Colaborador inativo')
            request.session['carrinho'] = []
            return redirect('cadastrar_compra')

        # Verifique se o carrinho está vazio
        if not carrinho_ids:
            messages.warning(request, 'O carrinho está vazio.')
            return render(request, 'registro.html')

        # Usar uma transação para salvar os itens do carrinho no banco de dados
        with transaction.atomic():
            # Criar uma nova instância de Compra para o colaborador
            compra = Compra.objects.create(colaborador=colaborador)

            # Dicionário para mapear os produtos e suas quantidades
            produtos_quantidades = {}

            # Calcular o preço total e as quantidades dos produtos
            preco = 0.0
            for produto_id in carrinho_ids:
                try:
                    produto = Produto.objects.get(pk=produto_id)

                    if produto in produtos_quantidades:
                        # Produto já existe no carrinho, incrementar a quantidade
                        produtos_quantidades[produto] += 1
                    else:
                        # Produto ainda não existe no carrinho, adicionar com quantidade 1
                        produtos_quantidades[produto] = 1

                    preco += float(produto.preco_produto)
                except Produto.DoesNotExist:
                    # Tratamento de erro caso o produto não seja encontrado
                    messages.warning(
                        request, f"Produto com ID {produto_id} não encontrado")

            # Criar os itens de compra com as quantidades dos produtos
            for produto, quantidade in produtos_quantidades.items():
                ItemCompra.objects.create(
                    compra=compra, produto=produto, quantidade=quantidade, preco_total=preco)

            compra.preco = preco
            compra.save()

        carrinho = []
        for produto_id in carrinho_ids:
            produto = Produto.objects.get(id=produto_id)
            carrinho.append(produto)

        # Limpar o carrinho após a finalização da compra
        request.session['carrinho'] = []
        carrinho_ids = []

        # Verifica se a compra não está zerada e se há mais de um item no carrinho
        valor_gasto_ultima_referencia = ValorReferenciaAnterior(colaborador)

        # Lógica para calcular o valor gasto na compra atual
        valor_gasto_compra_atual = valor_gasto_ultima_referencia + compra.preco
        messages.success(request, 'Compra efetuada com sucesso.')

        # Obtém os valores atualizados
        valor_gasto_ultima_referencia = ValorReferenciaAnterior(colaborador)
        valor_gasto_mes_atual = ValorReferenciaAtual(colaborador)

        # Deduzir os itens comprados do estoque
        for produto, quantidade in produtos_quantidades.items():
            try:
                estoque = Estoque.objects.get(produto=produto)
                estoque.quantidade -= quantidade
                estoque.save()
            except Estoque.DoesNotExist:
                messages.warning(request, f"Produto '{produto.nome}' não encontrado no estoque.")

        destinatario = colaborador.email
        assunto = 'Compra realizada com sucesso'
        mensagem = 'Sua compra foi efetuada com sucesso.'
        data_hora_atual = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        enviar_email(destinatario, assunto, mensagem,
                     carrinho, data_hora_atual, colaborador.nome)

        # Check if the purchased products include an "ingresso" type
        if any(produto.categoria == 'ingresso' for produto in carrinho):
            # Send a separate email to another person with the ticket information
            destinatario_ingresso = 'tatianibonecher@gmail.com'  # Replace with the actual recipient's email address
            assunto_ingresso = 'Ingresso adquirido'
            mensagem_ingresso = f'Você adquiriu um ingresso. Detalhes da compra:\n'

            # Add purchase details for the "ingresso" products
            for produto, quantidade in produtos_quantidades.items():
                if produto.categoria == 'ingresso':
                    mensagem_ingresso += f'Nome do ingresso: {produto.nome}\n'
                    mensagem_ingresso += f'Quantidade: {quantidade}\n'
                    mensagem_ingresso += f'Preço unitário: {produto.preco_produto}\n\n'

            send_mail(assunto_ingresso, mensagem_ingresso, 'testeacademia@sci.com.br', [destinatario_ingresso])

        return render(request, 'registro.html', {
            'valor_gasto_ultima_referencia': valor_gasto_ultima_referencia,
            'valor_gasto_mes_atual': valor_gasto_mes_atual,
            'data_hora_compra': data_hora_atual,
            'nome_colaborador': colaborador.nome
        })


def LimparCarrinho(request):
    request.session.pop('carrinho', None)
    messages.success(request, 'Carrinho limpo com sucesso.')
    return redirect('cadastrar_compra')


def ExcluirItem(request, item_id):
    carrinho = request.session.get('carrinho', [])
    if item_id in carrinho:
        carrinho.remove(item_id)
        request.session['carrinho'] = carrinho
        messages.success(request, 'Item removido do carrinho com sucesso.')
    else:
        messages.error(request, 'O item não está no carrinho.')

    return redirect('cadastrar_compra')


def ValorReferenciaAnterior(colaborador):
    # Lógica para calcular o valor gasto na referência anterior
    # Utilize o objeto colaborador para obter os dados necessários

    today = datetime.date.today()
    if today.day >= 25:
        referencia_anterior = today.replace(
            day=25) - datetime.timedelta(days=1)
    else:
        if today.month == 1:
            referencia_anterior = today.replace(
                year=today.year-1, month=12, day=25) - datetime.timedelta(days=1)
        else:
            referencia_anterior = today.replace(
                month=today.month-1, day=25) - datetime.timedelta(days=1)

    valor_gasto_referencia_anterior = Compra.objects.filter(
        colaborador=colaborador, data_compra__lte=referencia_anterior).aggregate(total=Sum('preco'))['total']

    if valor_gasto_referencia_anterior:
        return valor_gasto_referencia_anterior
    else:
        return 0


def ValorReferenciaAtual(colaborador):
    # Lógica para calcular o valor gasto no mês atual
    # Utilize o objeto colaborador e a data atual para obter os dados necessários

    data_atual = datetime.datetime.now()

    if data_atual.day >= 26:
        # Considerar as compras a partir do dia 26 do mês atual
        valor_gasto_mes_atual = Compra.objects.filter(
            colaborador=colaborador, data_compra__gte=data_atual.replace(day=26)).aggregate(total=Sum('preco'))['total']
    else:
        # Considerar todas as compras do mês atual
        valor_gasto_mes_atual = Compra.objects.filter(
            colaborador=colaborador, data_compra__month=data_atual.month).aggregate(total=Sum('preco'))['total']

    if valor_gasto_mes_atual:
        return valor_gasto_mes_atual
    else:
        return 0


def VisualizarGastos(request):
    login = request.POST.get('login')
    senha = request.POST.get('senha')

    # Verifique as credenciais do colaborador
    colaborador = None
    try:
        colaborador = Colaborador.objects.get(login=login)

        if not check_password(senha, colaborador.senha):
            raise Colaborador.DoesNotExist
    except Colaborador.DoesNotExist:
        messages.error(request, 'Credenciais inválidas')
        return redirect('cadastrar_compra')

    # Verifique a situação do colaborador apenas se o objeto colaborador for encontrado
    if colaborador.situacao == 'Inativo':
        messages.error(request, 'Colaborador inativo')
        return redirect('cadastrar_compra')

    # Obtém os valores de gastos
    valor_gasto_ultima_referencia = ValorReferenciaAnterior(colaborador)
    valor_gasto_mes_atual = ValorReferenciaAtual(colaborador)
    valor_gasto_compra_atual = valor_gasto_ultima_referencia + valor_gasto_mes_atual

    # Renderiza o template com os valores de gastos
    context = {
        'valor_gasto_ultima_referencia': valor_gasto_ultima_referencia,
        'valor_gasto_mes_atual': valor_gasto_mes_atual,
        'valor_gasto_compra_atual': valor_gasto_compra_atual,
    }
    return render(request, 'registro.html', context)


@login_required(login_url='login')
def ListarCompra(request):
    compras = Compra.objects.all()
    return render(request, 'listar_compras.html', {'compras': compras})


from django.db.models import Count

