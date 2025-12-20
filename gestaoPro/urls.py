from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from usuarios import views

urlpatterns = [
    path('admin/', admin.site.urls), # A rota do painel de controle
    path('', include('usuarios.urls')), # Conecta as páginas que criamos no app 'usuarios'
    path('clientes/', include('clientes.urls')), # Conecta as páginas que criamos no app 'clientes'
    path('ordens/', include('ordens.urls')), # Conecta as páginas que criamos no app 'ordens'
    path('cadastrar-funcionario/', views.cadastrar_funcionario, name='cadastrar_funcionario'),
    path('login/', auth_views.LoginView.as_view(template_name='usuarios/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('lista-funcionarios/', views.lista_funcionarios, name='lista_funcionarios'),
    path('cadastrar-funcionario/', views.cadastrar_funcionario, name='cadastrar_funcionario'),
    path('editar-funcionario/<int:user_id>/', views.editar_funcionario, name='editar_funcionario'),
    path('excluir-funcionario/<int:user_id>/', views.excluir_funcionario, name='excluir_funcionario'),
    path('configuracoes/', views.configuracoes_sistema, name='configuracoes_sistema'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)