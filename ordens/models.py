from django.db import models
from django.contrib.auth.models import User
from clientes.models import Cliente
from usuarios.models import Produto  # <--- IMPORTANTE: Importamos o Produto aqui

# Remova a classe Material que estava aqui. Não precisamos dela.

class OrdemServico(models.Model):
    STATUS_CHOICES = [
        ('PENDENTE', 'Aguardando Arte'),
        ('ARTE_PRODUCAO', 'Arte em Produção'),
        ('APROVACAO', 'Aguardando Cliente'),
        ('PRODUCAO', 'Em Produção'),
        ('FINALIZADO', 'Pronto para Entrega'),
        ('ENTREGUE', 'Entregue'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    vendedor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    # MUDANÇA AQUI: Agora aponta para Produto ao invés de Material
    material = models.ForeignKey(Produto, on_delete=models.SET_NULL, null=True, verbose_name="Material/Produto")
    
    altura = models.DecimalField(max_digits=5, decimal_places=2, help_text="Em metros (Ex: 1.00)")
    largura = models.DecimalField(max_digits=5, decimal_places=2, help_text="Em metros (Ex: 0.50)")
    quantidade = models.IntegerField(default=1)
    
    detalhes = models.TextField(blank=True, null=True, verbose_name="Observações da Arte")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDENTE')
    data_criacao = models.DateTimeField(auto_now_add=True)
    
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Valor Total")

    def save(self, *args, **kwargs):
        # Lógica de cálculo atualizada para usar 'preco_venda' do Produto
        if self.material and self.altura and self.largura:
            area = self.altura * self.largura
            # Aqui usamos 'preco_venda' que é o campo que vi no seu HTML de configurações
            preco_unitario = area * self.material.preco_venda 
            self.valor_total = preco_unitario * self.quantidade
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"OS {self.id} - {self.cliente.nome}"