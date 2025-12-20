from django.contrib import admin
from .models import Cliente

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    # Colunas que vão aparecer na listagem
    list_display = ('nome', 'whatsapp', 'cpf_cnpj', 'data_cadastro')
    # Campos que permitem busca
    search_fields = ('nome', 'cpf_cnpj')