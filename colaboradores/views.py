import logging
from django.core.exceptions import ValidationError
from colaboradores.forms import CadastrarColaboradorForm, EditarColaboradorForm
from .models import Colaborador
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password


@login_required(login_url='login')
def criar_colaboradores(request):
    if request.method == 'POST':
        form = CadastrarColaboradorForm(request.POST)
        if form.is_valid():


            # pode testar apresentando muita queryy
            

            
            nome = form.cleaned_data['nome']
            cpf = form.cleaned_data['cpf']
            login = form.cleaned_data['login']
            senha = form.cleaned_data['senha']
            confirmar_senha = form.cleaned_data['confirmar_senha']
            situacao = form.cleaned_data['situacao']

            if senha != confirmar_senha:
                messages.error(
                    request, 'A senha e a confirmação de senha não correspondem.')
                return redirect('criar_colaboradores')

            if Colaborador.objects.filter(cpf=cpf).exists():
                messages.error(request, 'CPF já cadastrado.')
                return redirect('criar_colaboradores')

            if Colaborador.objects.filter(login=login).exists():
                messages.error(request, 'Login já cadastrado.')
                return redirect('criar_colaboradores')

            try:
                # Criptografa a senha
                senha_criptografada = make_password(senha)

                # Salva o colaborador no banco de dados
                colaborador = Colaborador(
                    nome=nome, cpf=cpf, login=login, senha=senha_criptografada, situacao=situacao)
                colaborador.save()

                # Additional logic to create the collaborator with other fields
                # ...

                return redirect('listar_colaboradores')
            except ValidationError as e:
                error_message = "Erro de validação: " + str(e)
                return render(request, 'error.html', {'error_message': error_message})
            except Exception as e:
                error_message = "Ocorreu um erro ao criar o colaborador. Detalhes: " + \
                    str(e)
                logging.exception(error_message)
                return render(request, 'error.html', {'error_message': error_message})
    else:
        form = CadastrarColaboradorForm()

    return render(request, 'cadastro_colaborador.html', {'form': form})


@login_required(login_url='login')
def listar_colaboradores(request):
    colaboradores = Colaborador.objects.all()
    return render(request, 'listar_colaborador.html', {'colaboradores': colaboradores})

@login_required(login_url='login')
def editar_colaborador(request, colaborador_id):
    colaborador = get_object_or_404(Colaborador, id=colaborador_id)

    if request.method == 'POST':
        form = EditarColaboradorForm(request.POST, instance=colaborador)
        if form.is_valid():
            nome = form.cleaned_data['nome']
            cpf = form.cleaned_data['cpf']
            login = form.cleaned_data['login']
            senha = form.cleaned_data['senha']
            confirmar_senha = form.cleaned_data['confirmar_senha']
            situacao = form.cleaned_data['situacao']

            # Verificação concluída
            if Colaborador.objects.filter(cpf=cpf).exclude(id=colaborador_id).exists():
                messages.error(request, 'CPF já cadastrado.')
                return redirect('editar_colaborador', colaborador_id=colaborador_id)

            if senha != confirmar_senha:
                messages.error(request, 'A senha e a confirmação de senha não correspondem.')
                return redirect('editar_colaborador', colaborador_id=colaborador_id)

            # Verifica se a senha foi modificada
            if senha:
                # Criptografa a nova senha
                senha_criptografada = make_password(senha)
                colaborador.senha = senha_criptografada
            else:
                # Se a senha não foi modificada, define a senha atual do colaborador como vazia
                colaborador.senha = ''

            try:
                # Atualiza os dados do colaborador no banco de dados
                colaborador.nome = nome
                colaborador.cpf = cpf
                colaborador.login = login
                colaborador.situacao = situacao
                colaborador.save()

                # Additional logic to update other fields of the collaborator
                # ...

                return redirect('listar_colaboradores')
            except ValidationError as e:
                error_message = "Erro de validação: " + str(e)
                return render(request, 'error.html', {'error_message': error_message})
            except Exception as e:
                error_message = "Ocorreu um erro ao editar o colaborador. Detalhes: " + str(e)
                logging.exception(error_message)
                return render(request, 'error.html', {'error_message': error_message})
    else:
        # Se a requisição não for POST, passa a senha e a confirmação de senha como vazias para o formulário
        initial_data = {'senha': '', 'confirmar_senha': ''}
        form = EditarColaboradorForm(instance=colaborador, initial=initial_data)

        # Define a opção selecionada no campo de situação com base na situação atual do colaborador
        form.fields['situacao'].initial = colaborador.situacao

    return render(request, 'editar_colaborador.html', {'form': form, 'colaborador_id': colaborador_id})
