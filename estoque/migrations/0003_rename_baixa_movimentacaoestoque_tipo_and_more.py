# Generated by Django 4.2.2 on 2023-07-11 17:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('estoque', '0002_movimentacaoestoque'),
    ]

    operations = [
        migrations.RenameField(
            model_name='movimentacaoestoque',
            old_name='baixa',
            new_name='tipo',
        ),
        migrations.RemoveField(
            model_name='movimentacaoestoque',
            name='entrada',
        ),
    ]