
from django.db import models

from produtos.models import Produto

# Create your models here.

class Estoque(models.Model):
    produto = models.OneToOneField(Produto, on_delete=models.CASCADE)
    quantidade = models.IntegerField(default=0)
    

    def __str__(self):
     return f"{self.produto.nome} - {self.quantidade} unidades em estoque"
