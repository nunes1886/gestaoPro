from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
# Adicionamos os novos models aqui na importação
from .models import Setor, Perfil, ConfiguracaoSistema, Produto, StatusOS

# --- SEU FORMULÁRIO ANTIGO (MANTIDO) ---
class FuncionarioForm(UserCreationForm):
    setor = forms.ModelChoiceField(
        queryset=Setor.objects.all(),
        label="Setor / Hierarquia",
        empty_label="Selecione o Setor",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    cargo = forms.ChoiceField(
        label="Cargo / Função",
        choices=Perfil.CARGOS,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "setor", "cargo") 
        labels = {
            'username': 'Nome de Usuário (Login)',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.help_text = None


# --- NOVOS FORMULÁRIOS PARA A TELA DE CONFIGURAÇÃO ---

# 1. Formulário da Empresa (Card Cinza)
class ConfiguracaoForm(forms.ModelForm):
    class Meta:
        model = ConfiguracaoSistema
        fields = ['nome_empresa', 'cnpj', 'endereco', 'cep', 'telefone', 'logo', 'favicon']
        widgets = {
            'nome_empresa': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Nunes Sublimação'}),
            'cnpj': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '00.000.000/0001-00'}),
            'endereco': forms.TextInput(attrs={'class': 'form-control'}),
            'cep': forms.TextInput(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control'}),
            'logo': forms.FileInput(attrs={'class': 'form-control'}),
            'favicon': forms.FileInput(attrs={'class': 'form-control'}),
        }

# 2. Formulário de Produtos (Card Verde)
class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'preco_venda', 'preco_revenda']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Lona 440g'}),
            'preco_venda': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'preco_revenda': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

# 3. Formulário de Setor (Card Azul)
class SetorForm(forms.ModelForm):
    class Meta:
        model = Setor
        fields = ['nome']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do novo setor'}),
        }

# 4. Formulário de Status (Card Amarelo)
class StatusForm(forms.ModelForm):
    class Meta:
        model = StatusOS
        fields = ['nome', 'tipo']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Aguardando Arte'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
        }