

from django.db import models
from django.contrib.auth.models import User

from produtos.models import Produto
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Estoque(models.Model):
    produto = models.OneToOneField(Produto, on_delete=models.CASCADE)
    quantidade = models.IntegerField(default=0)
    

    def __str__(self):
     return f"{self.produto.nome} - {self.quantidade} unidades em estoque"



class MovimentacaoEstoque(models.Model):
    MOVIMENTO_CHOICES = (
        ('entrada', 'Entrada'),
        ('baixa', 'Baixa'),
    )

    tipo_movimentacao = models.CharField(choices=MOVIMENTO_CHOICES, max_length=10,default='entrada')
    quantidade = models.PositiveIntegerField(default=1)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    produto= models.ForeignKey(Produto,on_delete=models.CASCADE)
    data = models.DateTimeField(default=timezone.now)
    

    def __str__(self):
        return f"{self.tipo_movimentacao} de {self.quantidade} - {self.data}"