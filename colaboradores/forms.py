from django import forms
from django import forms
from .models import Colaborador

class CadastrarColaboradorForm(forms.Form):
    nome = forms.CharField(label='Nome')
    cpf = forms.CharField(label='CPF')
    login = forms.CharField(label='Login')
    email = forms.EmailField(label='Email') 
    senha = forms.CharField(label='Senha', widget=forms.PasswordInput)
    confirmar_senha = forms.CharField(label='Confirmar Senha', widget=forms.PasswordInput)
    situacao = forms.CharField(label='Situação')


class EditarColaboradorForm(forms.ModelForm):
    senha = forms.CharField(widget=forms.PasswordInput(render_value=True))
    confirmar_senha = forms.CharField(widget=forms.PasswordInput(render_value=True))

    class Meta:
        model = Colaborador
        fields = ['nome', 'cpf', 'login', 'email', 'senha', 'confirmar_senha', 'situacao']
        widgets = {
            'senha': forms.PasswordInput(render_value=True),
            'confirmar_senha': forms.PasswordInput(render_value=True)
        }
