from django import forms

from produtos.models import Produto


class CadastrarProdutos(forms.Form):
    nome = forms.CharField(label='Nome')
    codigo_barras = forms.CharField(label='Codigo_Barras')
    preco_produto = forms.CharField(label='Preco_Produto')
    situacao = forms.CharField(label='Situação')

class EditarProdutosForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'codigo_barras', 'preco_produto', 'situacao']