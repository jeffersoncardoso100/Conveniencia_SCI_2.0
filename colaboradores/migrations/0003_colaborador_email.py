# Generated by Django 4.2.2 on 2023-07-05 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('colaboradores', '0002_alter_colaborador_cpf_alter_colaborador_login'),
    ]

    operations = [
        migrations.AddField(
            model_name='colaborador',
            name='email',
            field=models.EmailField(max_length=254, null=True),
        ),
    ]