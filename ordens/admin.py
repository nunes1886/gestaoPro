from django.contrib import admin
from .models import OrdemServico

# Remova a importação de Material e o registro dele
# Se houver admin.site.register(Material), apague.

@admin.register(OrdemServico)
class OrdemServicoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'material', 'valor_total', 'status', 'data_criacao')
    list_filter = ('status', 'material')
    search_fields = ('cliente__nome', 'id')