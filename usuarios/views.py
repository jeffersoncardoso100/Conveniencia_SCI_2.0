from django.shortcuts import get_object_or_404, render

# Create your views here.

from telnetlib import LOGOUT
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test


def login_usuario(request):
    if request.user.is_authenticated:

        # Se o usuário já estiver autenticado, redireciona para a página inicial
        return redirect('home')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                # Autenticação bem-sucedida, redirecionar para uma página específica
                # Redirecionar para a URL nomeada 'home'
                return redirect('home')
            else:
                error_message = 'Credenciais inválidas.'
                # Autenticação falhou, exibir mensagem de erro na mesma página de login
                return render(request, 'login.html', {'error_message': error_message})
        except Exception as e:
            # Lidar com exceções durante a autenticação
            error_message = f"Ocorreu um erro durante a autenticação: {str(e)}"
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')


@login_required(login_url='login')
def home(request):
    return render(request, 'home.html')


# exeção aplicada apos revisão com o mentor
@login_required
def logout_view(request):
    try:
        logout(request)
    except Exception as e:
        # Trate a exceção aqui, como registrar o erro ou exibir uma mensagem de erro
        # Você pode personalizar essa parte com base nos seus requisitos
        print(f"Erro durante o logout: {str(e)}")

    return redirect('login')


@user_passes_test(lambda v: v.is_superuser, login_url='login')
@login_required
def cadastrar_usuario(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm-password')
            email = request.POST.get('email')

            # Verificar se o usuário já existe
            if User.objects.filter(username=username).exists():
                error_message = 'Nome de usuário já está em uso.'
                return render(request, 'cadastro.html', {'error_message': error_message})

            # Verificar se o email já está em uso
            if User.objects.filter(email=email).exists():
                error_message = 'O email já está em uso.'
                return render(request, 'cadastro.html', {'error_message': error_message})

            # Verificar se a senha e a confirmação de senha são iguais
            if password != confirm_password:
                error_message = 'A senha e a confirmação de senha não coincidem.'
                return render(request, 'cadastro.html', {'error_message': error_message})

            # Cria o usuário
            user = User.objects.create_user(
                username=username, password=password, email=email)

            # Autentica e faz login com o novo usuário

            # Redireciona para a página de perfil ou outra página desejada
            return redirect('listar_usuarios')

        except Exception as e:
            # Lidar com exceção, exibir mensagem de erro ou redirecionar para uma página de erro
            error_message = f'Ocorreu um erro durante o cadastro do usuário: {str(e)}'
            return render(request, 'cadastro.html', {'error_message': error_message})

    return render(request, 'cadastro.html')


@user_passes_test(lambda v: v.is_superuser, login_url='login')
@login_required
def listar_usuarios(request):
    usuarios = User.objects.all()  # Obtém todos os usuários do banco de dados
    return render(request, 'listar_usuarios.html', {'usuarios': usuarios})


def deletar_usuario(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return redirect('listar_usuarios')


@login_required
def editar_usuario(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            email = request.POST.get('email')

            # Verificar se o nome de usuário já está em uso por outro usuário
            if User.objects.filter(username=username).exclude(id=user_id).exists():
                error_message = 'Nome de usuário já está em uso.'
                return render(request, 'edicao.html', {'user': user, 'error_message': error_message})

            # Verificar se o email já está em uso por outro usuário
            if User.objects.filter(email=email).exclude(id=user_id).exists():
                error_message = 'O email já está em uso.'
                return render(request, 'edicao.html', {'user': user, 'error_message': error_message})

            # Atualizar os dados do usuário
            user.username = username
            user.email = email
            user.save()

            # Redirecionar para a página de perfil ou outra página desejada
            return redirect('listar_usuarios')

        except Exception as e:
            # Lidar com exceção, exibir mensagem de erro ou redirecionar para uma página de erro
            error_message = f'Ocorreu um erro durante a edição do usuário: {str(e)}'
            return render(request, 'edicao.html', {'user': user, 'error_message': error_message})

    return render(request, 'edicao.html', {'user': user})
