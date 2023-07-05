from django.db import models

# Create your models here.
from django.db import models

class Produto(models.Model):
    nome = models.CharField(max_length=100)
    codigo_barras = models.CharField(max_length=100)
    preco_produto = models.DecimalField(max_digits=10, decimal_places=2)
    situacao = models.CharField(max_length=50)
    
    def __str__(self):
        return self.nome

