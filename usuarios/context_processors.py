from .models import ConfiguracaoSistema

def configuracao_empresa(request):
    # Pega a primeira configuração cadastrada no banco
    config = ConfiguracaoSistema.objects.first()
    return {'config_projeto': config}