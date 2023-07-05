from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Compra, ItemCompra

# Register your models here.
admin.site.register(Compra)

admin.site.register(ItemCompra)