from django.contrib import admin
from .models import Perfil, ConfiguracaoSistema, Setor

# Lista de modelos que queremos registrar
modelos = [Perfil, ConfiguracaoSistema, Setor]

for modelo in modelos:
    try:
        admin.site.register(modelo)
    except admin.sites.AlreadyRegistered:
        # Se já estiver registrado, o Django ignora o erro e segue em frente
        pass