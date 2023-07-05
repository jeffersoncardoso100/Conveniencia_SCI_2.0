

from colaboradores import models
from produtos.models import Produto
from django.db import models
from colaboradores.models import Colaborador
from django.db import models

class Compra(models.Model):
    produtos = models.ManyToManyField(Produto, through='ItemCompra')
    data_compra = models.DateField(auto_now_add=True)
    colaborador = models.ForeignKey(Colaborador, on_delete=models.DO_NOTHING, null=True)
    preco= models.FloatField(null=True)

class ItemCompra(models.Model):
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1)
    preco_total= models.FloatField(null=True)

    def __str__(self):
        return f"Compra #{self.compra.pk} - Produto: {self.produto.nome}, Quantidade: {self.quantidade}"
    

