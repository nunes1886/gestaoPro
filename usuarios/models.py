from django.db import models
from django.contrib.auth.models import User

# --- 1. SETORES (Hierarquia) ---
class Setor(models.Model):
    nome = models.CharField(max_length=100)
    pode_ver_financeiro = models.BooleanField(default=False)
    pode_ver_clientes = models.BooleanField(default=True)
    pode_ver_ordens = models.BooleanField(default=True)
    pode_gerir_equipe = models.BooleanField(default=False)

    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name = "Setor"
        verbose_name_plural = "Setores"

# --- 2. PRODUTOS E PREÇOS (Novo) ---
class Produto(models.Model):
    nome = models.CharField(max_length=100)
    # Preço de Venda (quanto o cliente paga)
    preco_venda = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    # Preço de Revenda (para parceiros, se houver)
    preco_revenda = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.nome

# --- 3. STATUS DA O.S. (Novo) ---
class StatusOS(models.Model):
    # Tipos para o sistema entender a lógica (não apenas o nome visual)
    TIPOS = [
        ('aberto', 'Aberto / Na Fila'),
        ('em_producao', 'Em Produção'),
        ('finalizado', 'Finalizado / Pronto'),
        ('cancelado', 'Cancelado'),
    ]
    nome = models.CharField(max_length=50) # O nome que você cria (ex: "Aguardando Arte")
    tipo = models.CharField(max_length=20, choices=TIPOS, default='aberto')
    cor = models.CharField(max_length=7, default="#6c757d") # Para ficar colorido no dashboard (opcional)

    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name = "Status de OS"
        verbose_name_plural = "Status de OS"

# --- 4. PERFIL DO USUÁRIO ---
class Perfil(models.Model):
    CARGOS = [
        ('AUXILIAR', 'Auxiliar'),
        ('OPERADOR', 'Operador'),
        ('GERENTE', 'Gerente'),
        ('DIRETOR', 'Diretor'),
        ('DONO', 'Proprietário'),
    ]

    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    setor = models.ForeignKey(Setor, on_delete=models.SET_NULL, null=True, blank=True)
    cargo = models.CharField(max_length=20, choices=CARGOS, default='AUXILIAR')
    data_nascimento = models.DateField(null=True, blank=True)
    foto = models.ImageField(upload_to='perfil/', null=True, blank=True)

    def __str__(self):
        setor_nome = self.setor.nome if self.setor else "Sem Setor"
        return f"{self.usuario.username} - {self.get_cargo_display()} ({setor_nome})"

# --- 5. CONFIGURAÇÃO DO SISTEMA (Atualizado) ---
class ConfiguracaoSistema(models.Model):
    # Dados Básicos
    nome_empresa = models.CharField(max_length=100, default="GestãoPro")
    
    # Dados de Contato e Fiscais (Adicionados para o Card "Dados da Empresa")
    cnpj = models.CharField(max_length=20, null=True, blank=True)
    endereco = models.CharField(max_length=255, null=True, blank=True)
    cep = models.CharField(max_length=20, null=True, blank=True)
    telefone = models.CharField(max_length=20, null=True, blank=True)
    
    # Imagens
    logo = models.ImageField(upload_to='configuracao/', null=True, blank=True)
    favicon = models.ImageField(upload_to='configuracao/', null=True, blank=True)

    def __str__(self):
        return self.nome_empresa

    class Meta:
        verbose_name = "Configuração do Sistema"
        verbose_name_plural = "Configurações do Sistema"