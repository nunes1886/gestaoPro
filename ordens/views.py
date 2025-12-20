from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import OrdemServico
from .forms import OrdemServicoForm
from django.db.models import Sum
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

@login_required
def lista_ordens(request):
    ordens = OrdemServico.objects.all().order_by('-data_criacao')
    return render(request, 'ordens/lista_ordens.html', {'ordens': ordens})

def nova_ordem(request):
    if request.method == 'POST':
        form = OrdemServicoForm(request.POST)
        if form.is_valid():
            os = form.save(commit=False)
            os.vendedor = request.user  # Registra quem está criando a OS
            os.save()
            return redirect('lista_ordens')
    else:
        form = OrdemServicoForm()
    return render(request, 'ordens/form_ordem.html', {'form': form})

@login_required
def setor_arte(request):
    # Filtra apenas as OS que precisam de atenção da arte
    ordens_arte = OrdemServico.objects.filter(
        status__in=['PENDENTE', 'ARTE_PRODUCAO', 'APROVACAO']
    ).order_by('data_criacao')
    
    return render(request, 'ordens/setor_arte.html', {'ordens': ordens_arte})


@login_required
def financeiro_view(request):
    vendas = OrdemServico.objects.all()
    
    # 1. Capturar as datas do formulário (filtro)
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')
    
    # 2. Aplicar o filtro se as datas existirem
    if data_inicio and data_fim:
        # Filtra as ordens criadas entre as duas datas
        vendas = vendas.filter(data_criacao__range=[data_inicio, data_fim])

    # 3. Cálculos baseados no que foi filtrado
    total_vendas = vendas.aggregate(Sum('valor'))['valor__sum'] or 0
    recebido = vendas.filter(status='ENTREGUE').aggregate(Sum('valor'))['valor__sum'] or 0
    a_receber = total_vendas - recebido
    
    # Pegar as últimas 5 do filtro
    ultimas_os = vendas.order_by('-id')[:5]
    
    contexto = {
        'total_vendas': total_vendas,
        'recebido': recebido,
        'a_receber': a_receber,
        'ultimas_os': ultimas_os,
        'data_inicio': data_inicio, # Devolvemos para o HTML manter o campo preenchido
        'data_fim': data_fim,
    }
    return render(request, 'ordens/financeiro.html', contexto)

@login_required
def gerar_pdf_ordem(request, os_id):
    # Pega os dados da OS
    os = OrdemServico.objects.get(id=os_id)
    
    # Cria o objeto de resposta como PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="OS_{os.id}.pdf"'

    # Desenha o PDF
    p = canvas.Canvas(response, pagesize=A4)
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, 800, f"ORDEM DE SERVIÇO #{os.id}")
    
    p.setFont("Helvetica", 12)
    p.drawString(100, 770, f"Cliente: {os.cliente.nome}")
    p.drawString(100, 750, f"Serviço: {os.servico}")
    p.drawString(100, 730, f"Valor: R$ {os.valor}")
    p.drawString(100, 710, f"Status: {os.get_status_display()}")
    
    p.line(100, 700, 500, 700) # Linha divisória
    
    p.drawString(100, 680, "Detalhes:")
    p.drawString(100, 660, f"{os.detalhes or 'Sem observações.'}")

    p.showPage()
    p.save()
    return response