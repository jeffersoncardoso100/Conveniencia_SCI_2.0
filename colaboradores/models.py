from django.db import models

class Colaborador(models.Model):
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=14)
    login = models.CharField(max_length=50)
    senha = models.CharField(max_length=50)
    situacao = models.CharField(max_length=50)
    email = models.EmailField(max_length=254, null=True)
    

    def __str__(self):
        return self.nome
