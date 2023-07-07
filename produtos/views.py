from datetime import datetime
from operator import countOf
from xhtml2pdf import pisa
from io import BytesIO
import decimal
from django.forms import ValidationError
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from colaboradores.models import Colaborador
from produtos.forms import CadastrarProdutos
from produtos.models import Produto
from produtos.forms import EditarProdutosForm
from decimal import Decimal
from registro_de_compras.models import Compra, ItemCompra
from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from io import BytesIO
from datetime import datetime
from django.shortcuts import render, HttpResponse
from django.http import Http404
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Spacer, Paragraph, Table, TableStyle


@login_required(login_url='login')
def cadastro_produtos(request):
    if request.method == 'POST':
        form = CadastrarProdutos(request.POST)
        if form.is_valid():
            nome = form.cleaned_data['nome']
            codigo_barras = form.cleaned_data['codigo_barras']
            preco_produto = form.cleaned_data['preco_produto']
            situacao = form.cleaned_data['situacao']
            categoria = form.cleaned_data['categoria']

            try:
                # Verificar se o código de barras já existe no banco de dados
                if Produto.objects.filter(codigo_barras=codigo_barras).exists():
                    raise ValueError("Código de barras já cadastrado.")

                # Verificar se o valor do produto é válido
                try:
                    preco_produto = Decimal(preco_produto.replace(',', '.'))  # Substitui a vírgula por ponto
                except decimal.InvalidOperation:
                    raise ValueError("Valor do produto inválido.")

                # Criar e salvar o produto com a situação definida pelo usuário
                produto = Produto(
                    nome=nome, codigo_barras=codigo_barras, preco_produto=preco_produto, situacao=situacao, categoria=categoria)
                produto.save()

                # Redirecionar para a página de sucesso
                # Substitua 'listar_produtos' pela URL ou nome da página de listagem de produtos
                return redirect('listar_produtos')

            except ValueError as ve:
                # Lidar com erros relacionados a valores inválidos
                form.add_error('preco_produto', str(ve))

            except Exception as e:
                # Lidar com outras exceções
                mensagem_erro = f"Ocorreu um erro: {str(e)}"
                return render(request, 'error.html', {'mensagem_erro': mensagem_erro})

    else:
        form = CadastrarProdutos()

    return render(request, 'cadastro_produto.html', {'form': form})

@login_required(login_url='login')
def listar_produtos(request):
    produtos = Produto.objects.all()
    return render(request, 'listar_produtos.html', {'produtos': produtos})


@login_required(login_url='login')
def editar_produto(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)

    if request.method == 'POST':
        form = EditarProdutosForm(request.POST)
        if form.is_valid():
            try:
                # Processar os dados do formulário e salvar as alterações no objeto do produto
                produto.nome = form.cleaned_data['nome']
                produto.codigo_barras = form.cleaned_data['codigo_barras']
                produto.preco_produto = form.cleaned_data['preco_produto']
                produto.situacao = form.cleaned_data['situacao']
                produto.categoria = form.cleaned_data['categoria']

                # Verificar se o novo código de barras já está em uso por outro produto
                if Produto.objects.filter(codigo_barras=produto.codigo_barras).exclude(id=produto_id).exists():
                    raise ValidationError('Código de barras já está em uso por outro produto.')

                produto.save()

                # Redirecionar para outra página ou fazer qualquer outra ação necessária
                return redirect('listar_produtos')
            except ValidationError as e:
                # Lidar com a exceção de validação específica
                error_message = str(e)
                return render(request, 'editar_produto.html', {'form': form, 'produto': produto, 'error_message': error_message})
            except Exception as e:
                # Lidar com exceções genéricas
                error_message = f"Ocorreu um erro ao editar o produto: {str(e)}"
                return render(request, 'editar_produto.html', {'form': form, 'produto': produto, 'error_message': error_message})
    else:
        form = EditarProdutosForm(initial={
            'nome': produto.nome,
            'codigo_barras': produto.codigo_barras,
            'preco_produto': produto.preco_produto,
            'situacao': produto.situacao,
            'categoria':produto.categoria
        })

    context = {
        'form': form,
        'produto': produto,
    }

    return render(request, 'editar_produto.html', context)


@login_required(login_url='login')
def relatorio_compras_pdf(request):
    # Recuperar todas as compras do banco de dados
    compras = Compra.objects.all()

    # Definir o nome do arquivo PDF
    filename = 'relatorio_compras.pdf'

    # Renderizar o modelo HTML com os dados das compras
    template_path = 'relatorio_compras.html'
    context = {'compras': compras}

    # Renderizar o template HTML
    template = get_template(template_path)
    html = template.render(context)

    # Criar um objeto BytesIO para armazenar o PDF gerado
    result = BytesIO()

    # Converter o modelo HTML em PDF
    pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)

    # Configurar o response do Django com o tipo de conteúdo PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    # Obter o conteúdo do BytesIO e escrever no response
    response.write(result.getvalue())

    return response


@login_required(login_url='login')


def relatorio_personalizado(request):
    if request.method == 'POST':
        colaborador_id = request.POST.get('colaborador')
        data_inicio = request.POST.get('data_inicio')
        data_fim = request.POST.get('data_fim')

        # Verificar se os parâmetros de data são válidos
        try:
            data_inicio = datetime.strptime(data_inicio, '%Y-%m-%d').date()
            data_fim = datetime.strptime(data_fim, '%Y-%m-%d').date()
        except ValueError:
            return HttpResponse("Datas inválidas.")

        if colaborador_id == 'todos':
            colaborador = None
            compras = Compra.objects.filter(data_compra__range=[data_inicio, data_fim])
        else:
            try:
                # Verificar se o colaborador existe
                colaborador = Colaborador.objects.get(id=colaborador_id)
                compras = Compra.objects.filter(
                    colaborador=colaborador, data_compra__range=[data_inicio, data_fim])
            except Colaborador.DoesNotExist:
                raise Http404("Colaborador não encontrado.")

        # Cria o documento PDF
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []

        # Define estilos para o relatório
        styles = getSampleStyleSheet()
        estilo_titulo = ParagraphStyle(name='Titulo', parent=styles['Title'])
        estilo_paragrafo = styles['BodyText']

        # Preenche as informações do relatório
        titulo = Paragraph('Relatório de Compras', estilo_titulo)
        elements.append(titulo)

        # Adiciona quebras de linha
        elements.append(Spacer(1, 12))

        # Adiciona informações do colaborador e período de compra
        if colaborador:
            nome_colaborador = colaborador.nome
        else:
            nome_colaborador = "Todos os colaboradores"
        periodo_compra = f'Período de Compra: {data_inicio} a {data_fim}'

        # Adiciona as informações acima em um parágrafo
        paragrafo = Paragraph(
            f'Colaborador: {nome_colaborador}<br/>{periodo_compra}', estilo_paragrafo)
        elements.append(paragrafo)

        # Adiciona quebras de linha
        elements.append(Spacer(1, 12))

        # Cria a tabela de compras
        data = [['ID Compra', 'Data', 'Colaborador', 'Produto', 'Quantidade', 'Preço']]

        for compra in compras:
            produtos_compra = ItemCompra.objects.filter(compra=compra)

            for produto_compra in produtos_compra:
                data.append([
                    str(compra.pk),
                    str(compra.data_compra),
                    str(compra.colaborador.nome),
                    str(produto_compra.produto.nome),
                    str(produto_compra.quantidade),
                    str(produto_compra.preco_total)
                ])

        tabela = Table(data)
        tabela.setStyle(TableStyle([

            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(tabela)

        # Constrói o documento PDF
        doc.build(elements)

        # Define o cabeçalho Content-Disposition para fazer o download do arquivo
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="relatorio_colaborador.pdf"'

        # Salva o conteúdo do PDF na resposta HTTP
        response.write(buffer.getvalue())

        return response

    colaboradores = Colaborador.objects.all()
    return render(request, 'relatorio_pers.html', {'colaboradores': colaboradores})

@login_required(login_url='login')
def gerar_relatorio_geral(request):
    formato = request.GET.get('formato', '')
    download = request.GET.get('download', False)
    compras = Compra.objects.all()

    if formato == 'pdf':
        response = HttpResponse(content_type='application/pdf')
        filename = 'relatorio.pdf'
        doc = SimpleDocTemplate(response, pagesize=letter)
        elements = []
        data = []
        header = ['ID Compra', 'Data', 'Colaborador',
                  'Produto', 'Quantidade', 'Preço']
        data.append(header)

        for compra in compras:
            produtos_compra = ItemCompra.objects.filter(compra=compra)
            for produto_compra in produtos_compra:
                row = [
                    str(compra.pk),
                    str(compra.data_compra),
                    str(compra.colaborador),
                    str(produto_compra.produto.nome),
                    str(produto_compra.quantidade),
                    str(produto_compra.preco_total)
                ]
                data.append(row)

        table = Table(data)
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ])
        
        table.setStyle(style)
        elements.append(table)
        titulo = 'Relatório de Compras'
        titulo_paragraph = Paragraph(titulo, style=ParagraphStyle(name='Heading1', fontSize=18, spaceAfter=12))
        elements.insert(0, titulo_paragraph)

        doc.build(elements)

        if download:
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
        else:
            response['Content-Disposition'] = f'inline; filename="{filename}"'
    else:
        return HttpResponse('Formato de relatório inválido.')

    return response


"""@login_required(login_url='login')
def listar_mais_vendidos(request):
    produtos_mais_vendidos = Produto.objects.annotate(total_vendido=countOf('itemcompra')).order_by('')[:5]

    return render(request, 'maisvendidos.html', {'produtos_mais_vendidos': produtos_mais_vendidos})

from datetime import date

@login_required(login_url='login')
def ListarCompra(request):
    today = date.today()
    compras = Compra.objects.filter(data_hora__date=today)
    return render(request, 'listar_compras.html', {'compras': compras})
 """