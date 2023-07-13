from django.contrib import admin
from .models import Estoque
from .models import MovimentacaoEstoque


admin.site.register( Estoque)

admin.site.register(MovimentacaoEstoque)

# Register your models here.
