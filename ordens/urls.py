from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_ordens, name='lista_ordens'),
    path('nova/', views.nova_ordem, name='nova_ordem'),
    path('setor-arte/', views.setor_arte, name='setor_arte'),
    path('financeiro/', views.financeiro_view, name='financeiro'),
    path('ordem/pdf/<int:os_id>/', views.gerar_pdf_ordem, name='gerar_pdf_ordem'),
]