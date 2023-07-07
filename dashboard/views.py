from itertools import count
from operator import countOf
from django.shortcuts import render

from django.contrib.auth.decorators import login_required

from collections import Counter

from requests import request
from produtos.models import Produto

from registro_de_compras.models import Compra, ItemCompra



@login_required(login_url='login')
def home(request):
    return render(request, 'home.html')



