import logging
from django.core.exceptions import ValidationError
from colaboradores.forms import CadastrarColaboradorForm, EditarColaboradorForm
from .models import Colaborador
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError


@login_required(login_url='login')

def criar_colaboradores(request):
    if request.method == 'POST':
        form = CadastrarColaboradorForm(request.POST)
        if form.is_valid():
            nome = form.cleaned_data['nome']
            cpf = form.cleaned_data['cpf']
            login = form.cleaned_data['login']
            email = form.cleaned_data['email']
            senha = form.cleaned_data['senha']
            confirmar_senha = form.cleaned_data['confirmar_senha']
            situacao = form.cleaned_data['situacao']

            # Check if password and confirmation match
            if senha != confirmar_senha:
                messages.error(request, 'A senha e a confirmação de senha não correspondem.')
                return redirect('criar_colaboradores')

            # Check if CPF or login already exists
            if Colaborador.objects.filter(cpf=cpf).exists():
                messages.error(request, 'CPF já cadastrado.')
                return redirect('criar_colaboradores')

            if Colaborador.objects.filter(login=login).exists():
                messages.error(request, 'Login já cadastrado.')
                return redirect('criar_colaboradores')

            # Check if email already exists
            if Colaborador.objects.filter(email=email).exists():
                messages.error(request, 'Email já cadastrado.')
                return redirect('criar_colaboradores')

            try:
                # Validate the email
                email_validator = EmailValidator()
                email_validator(email)

                # Encrypt the password
                senha_criptografada = make_password(senha)

                # Save the collaborator in the database
                colaborador = Colaborador(
                    nome=nome, cpf=cpf, login=login, email=email, senha=senha_criptografada, situacao=situacao
                )
                colaborador.save()

                # Additional logic to create the collaborator with other fields
                # ...

                return redirect('listar_colaboradores')
            except ValidationError as e:
                error_message = "Erro de validação: " + str(e)
                return render(request, 'error.html', {'error_message': error_message})
            except Exception as e:
                error_message = "Ocorreu um erro ao criar o colaborador. Detalhes: " + str(e)
                logging.exception(error_message)
                return render(request, 'error.html', {'error_message': error_message})
    else:
        form = CadastrarColaboradorForm()

    return render(request, 'cadastro_colaborador.html', {'form': form})



@login_required(login_url='login')
def listar_colaboradores(request):
    colaboradores = Colaborador.objects.all()
    
        
    return render(request, 'listar_colaborador.html', {'colaboradores': colaboradores})




@login_required
def visualizar_colaborador(request, colaborador_id):
    colaborador = get_object_or_404(Colaborador, id=colaborador_id)
    
    return render(request, 'visualizar_colab.html', {'colaborador': colaborador})


@login_required(login_url='login')
def editar_colaborador(request, colaborador_id):
    colaborador = get_object_or_404(Colaborador, id=colaborador_id)

    if request.method == 'POST':
        form = EditarColaboradorForm(request.POST, instance=colaborador)
        if form.is_valid():
            nome = form.cleaned_data['nome']
            cpf = form.cleaned_data['cpf']
            login = form.cleaned_data['login']
            email = form.cleaned_data['email']
            senha = form.cleaned_data['senha']
            confirmar_senha = form.cleaned_data['confirmar_senha']
            situacao = form.cleaned_data['situacao']

            if Colaborador.objects.filter(cpf=cpf).exclude(id=colaborador_id).exists():
                messages.error(request, 'CPF já cadastrado.')
                return redirect('editar_colaborador', colaborador_id=colaborador_id)

            if Colaborador.objects.filter(email=email).exclude(id=colaborador_id).exists():
                messages.error(request, 'Email já cadastrado.')
                return redirect('editar_colaborador', colaborador_id=colaborador_id)

            if senha != confirmar_senha:
                messages.error(request, 'A senha e a confirmação de senha não correspondem.')
                return redirect('editar_colaborador', colaborador_id=colaborador_id)

            # Rest of your code for updating the collaborator

            try:
                # Atualiza os dados do colaborador no banco de dados
                colaborador.nome = nome
                colaborador.cpf = cpf
                colaborador.login = login
                colaborador.email = email
                colaborador.situacao = situacao

                # Verifica se a senha foi modificada
                if senha:
                    # Criptografa a nova senha
                    senha_criptografada = make_password(senha)
                    colaborador.senha = senha_criptografada

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
        # If the request is a GET request, provide the initial form data
        initial_data = {
            'senha': '',
            'confirmar_senha': '',
            'email': colaborador.email
        }
        form = EditarColaboradorForm(instance=colaborador, initial=initial_data)

        # Define the option selected in the 'situacao' field based on the current collaborator's situation
        form.fields['situacao'].initial = colaborador.situacao

    return render(request, 'editar_colaborador.html', {'form': form, 'colaborador_id': colaborador_id})
