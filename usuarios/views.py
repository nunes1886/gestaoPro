from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.db.models import Sum
from datetime import date

# Importação dos Models e Forms
from .models import Perfil, ConfiguracaoSistema, Produto, Setor, StatusOS
from ordens.models import OrdemServico
from clientes.models import Cliente  # <--- IMPORTANTE: Adicionado para o Reset funcionar
from .forms import FuncionarioForm, ConfiguracaoForm, ProdutoForm, SetorForm, StatusForm

def login_view(request):
    if request.method == 'POST':
        usuario_post = request.POST.get('username')
        senha_post = request.POST.get('password')
        user = authenticate(request, username=usuario_post, password=senha_post)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Usuário ou senha inválidos')
            
    return render(request, 'usuarios/login.html')

@login_required
def home_view(request):
    try:
        perfil = Perfil.objects.get(usuario=request.user)
    except Perfil.DoesNotExist:
        perfil = None

    mes_atual = date.today().month
    aniversariantes = Perfil.objects.filter(data_nascimento__month=mes_atual)
    
    # Cálculos para o Dashboard
    total_os = OrdemServico.objects.count()
    valor_total = OrdemServico.objects.aggregate(Sum('valor_total'))['valor_total__sum'] or 0
    os_pendentes = OrdemServico.objects.filter(status='PENDENTE').count()

    context = {
        'perfil': perfil,
        'aniversariantes': aniversariantes,
        'total_os': total_os,
        'valor_total': valor_total,
        'os_pendentes': os_pendentes,
    }
    return render(request, 'usuarios/home.html', context)

def logout_view(request):
    logout(request)
    return redirect('login')

# --- GESTÃO DE FUNCIONÁRIOS ---

@login_required
@staff_member_required
def cadastrar_funcionario(request):
    if request.method == 'POST':
        form = FuncionarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Dados extras do formulário
            setor_escolhido = form.cleaned_data.get('setor')
            cargo_escolhido = form.cleaned_data.get('cargo')

            # Cria ou atualiza o Perfil
            perfil, created = Perfil.objects.get_or_create(usuario=user)
            perfil.setor = setor_escolhido
            perfil.cargo = cargo_escolhido
            perfil.save()

            messages.success(request, f'Funcionário {user.username} cadastrado com sucesso!')
            return redirect('lista_funcionarios')
    else:
        form = FuncionarioForm()
    return render(request, 'usuarios/cadastrar_funcionario.html', {'form': form})

@login_required
@staff_member_required
def lista_funcionarios(request):
    funcionarios = User.objects.all()
    return render(request, 'usuarios/lista_funcionarios.html', {'funcionarios': funcionarios})

@login_required
@staff_member_required
def editar_funcionario(request, user_id):
    funcionario = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = FuncionarioForm(request.POST, instance=funcionario)
        if form.is_valid():
            form.save()
            # Atualiza também o perfil se necessário
            if hasattr(funcionario, 'perfil'):
                funcionario.perfil.setor = form.cleaned_data['setor']
                funcionario.perfil.cargo = form.cleaned_data['cargo']
                funcionario.perfil.save()
                
            messages.success(request, f'Dados de {funcionario.username} atualizados!')
            return redirect('lista_funcionarios')
    else:
        form = FuncionarioForm(instance=funcionario)
        # Preenche os campos iniciais com dados do perfil
        if hasattr(funcionario, 'perfil'):
            form.initial['setor'] = funcionario.perfil.setor
            form.initial['cargo'] = funcionario.perfil.cargo
            
    return render(request, 'usuarios/cadastrar_funcionario.html', {'form': form, 'editando': True})

@login_required
@staff_member_required
def excluir_funcionario(request, user_id):
    funcionario = get_object_or_404(User, id=user_id)
    if funcionario.is_superuser:
        messages.error(request, 'Não é possível excluir um administrador do sistema.')
    else:
        funcionario.delete()
        messages.success(request, 'Funcionário removido com sucesso.')
    return redirect('lista_funcionarios')

# --- NOVA TELA DE CONFIGURAÇÕES (CARDS + RESET + BACKUP) ---

@login_required
@staff_member_required
def configuracoes_sistema(request):
    # Pega a configuração (cria se não existir)
    config, created = ConfiguracaoSistema.objects.get_or_create(id=1)
    
    # Inicializa os forms
    form_config = ConfiguracaoForm(instance=config)
    form_produto = ProdutoForm()
    form_setor = SetorForm()
    form_status = StatusForm()

    if request.method == 'POST':
        # 1. Se clicou em "Salvar Dados da Empresa"
        if 'btn_empresa' in request.POST:
            form_config = ConfiguracaoForm(request.POST, request.FILES, instance=config)
            if form_config.is_valid():
                form_config.save()
                messages.success(request, "Dados da empresa atualizados!")
                return redirect('configuracoes_sistema')

        # 2. Se clicou em "Adicionar Produto"
        elif 'btn_produto' in request.POST:
            form_produto = ProdutoForm(request.POST)
            if form_produto.is_valid():
                form_produto.save()
                messages.success(request, "Produto adicionado!")
                return redirect('configuracoes_sistema')

        # 3. Se clicou em "Novo Setor"
        elif 'btn_setor' in request.POST:
            form_setor = SetorForm(request.POST)
            if form_setor.is_valid():
                form_setor.save()
                messages.success(request, "Setor criado!")
                return redirect('configuracoes_sistema')
        
        # 4. Se clicou em "Novo Status"
        elif 'btn_status' in request.POST:
            form_status = StatusForm(request.POST)
            if form_status.is_valid():
                form_status.save()
                messages.success(request, "Status adicionado!")
                return redirect('configuracoes_sistema')

        # 5. Se enviou arquivo de BACKUP (Restore)
        elif 'btn_restore' in request.POST:
            if request.FILES.get('arquivo_backup'):
                arquivo = request.FILES.get('arquivo_backup')
                # Lógica de restauração simulada para segurança na demo
                messages.warning(request, f"Arquivo '{arquivo.name}' recebido! (Restauração simulada)")
                return redirect('configuracoes_sistema')
            else:
                messages.error(request, "Nenhum arquivo selecionado.")

        # 6. Se clicou em RESET DE FÁBRICA (Com senha)
        elif 'btn_reset' in request.POST:
            senha_admin = request.POST.get('senha_confirmacao')
            
            # Verifica se a senha confere com a do usuário logado
            if request.user.check_password(senha_admin):
                try:
                    # Apaga TODAS as Ordens e Clientes
                    OrdemServico.objects.all().delete()
                    Cliente.objects.all().delete()
                    
                    messages.success(request, "Sistema resetado com sucesso! Dados limpos.")
                except Exception as e:
                    messages.error(request, f"Erro ao resetar: {e}")
            else:
                messages.error(request, "Senha incorreta! O reset foi cancelado.")
            
            return redirect('configuracoes_sistema')

    # Carrega as listas para exibir nas tabelas
    produtos = Produto.objects.all()
    setores = Setor.objects.all()
    lista_status = StatusOS.objects.all()

    context = {
        'form_config': form_config,
        'form_produto': form_produto,
        'form_setor': form_setor,
        'form_status': form_status,
        'produtos': produtos,
        'setores': setores,
        'lista_status': lista_status,
        'config': config 
    }
    return render(request, 'usuarios/configuracoes.html', context)

# Função para deletar itens dos cards (Botão X)
@login_required
def deletar_item(request, tipo, item_id):
    if tipo == 'produto':
        get_object_or_404(Produto, id=item_id).delete()
    elif tipo == 'setor':
        get_object_or_404(Setor, id=item_id).delete()
    elif tipo == 'status':
        get_object_or_404(StatusOS, id=item_id).delete()
    
    messages.success(request, "Item removido com sucesso.")
    return redirect('configuracoes_sistema')