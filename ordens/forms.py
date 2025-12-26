from django import forms
from .models import OrdemServico
from usuarios.models import Produto # <--- Importamos Produto

class OrdemServicoForm(forms.ModelForm):
    # Ajustamos o QuerySet para buscar em Produto
    material = forms.ModelChoiceField(
        queryset=Produto.objects.all(), # <--- Agora busca os produtos cadastrados
        required=True,
        label="Material",
        empty_label="Selecione o Material",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = OrdemServico
        # O resto continua igual...
        fields = ['cliente', 'material', 'altura', 'largura', 'quantidade', 'detalhes', 'status', 'valor_total']
        
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-select'}),
            'altura': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 1.00 (Metros)', 'step': '0.01', 'id': 'id_altura'}),
            'largura': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 0.50 (Metros)', 'step': '0.01', 'id': 'id_largura'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control', 'id': 'id_quantidade'}),
            'detalhes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'valor_total': forms.NumberInput(attrs={'class': 'form-control', 'id': 'id_valor_total', 'readonly': 'readonly'}),
        }