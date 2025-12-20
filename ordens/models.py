from django.db import models
from django.contrib.auth.models import User
from clientes.models import Cliente

class OrdemServico(models.Model):
    STATUS_CHOICES = [
        ('PENDENTE', 'Aguardando Arte'),
        ('ARTE_PRODUCAO', 'Arte em Produção'),
        ('APROVACAO', 'Aguardando Cliente'),
        ('PRODUCAO', 'Em Produção (Estamparia)'),
        ('FINALIZADO', 'Pronto para Entrega'),
        ('ENTREGUE', 'Entregue'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    vendedor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    servico = models.CharField(max_length=200, verbose_name="Produto/Serviço")
    detalhes = models.TextField(blank=True, null=True, verbose_name="Observações da Arte")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDENTE')
    data_criacao = models.DateTimeField(auto_now_add=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"OS {self.id} - {self.cliente.nome}"