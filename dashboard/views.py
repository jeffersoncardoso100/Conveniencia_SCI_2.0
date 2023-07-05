from itertools import count
from django.shortcuts import render

from django.contrib.auth.decorators import login_required

from collections import Counter

from registro_de_compras.models import Compra, ItemCompra



@login_required(login_url='login')
def home(request):
    return render(request, 'home.html')
