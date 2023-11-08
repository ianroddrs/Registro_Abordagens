from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name="login"),
    path('sair/', views.sair, name='sair'),
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('registros/acoes/', views.reg_acoes, name='reg_acoes'),
    path('registros/acoes/<int:id>/', views.reg_acao, name='reg_acao'),
    path('registros/operacoes/', views.reg_operacoes, name='reg_operacoes'),
    path('cadastro/usuario/', views.usuario, name='usuario'),
    path('cadastro/operacao/', views.cad_operacao, name='cad_operacao'),
    path('cadastro/acoes/', views.acoes, name='acoes'),
    path('cadastro/acoes/abordagem/', views.cad_abordagem, name='cad_abordagem'),
    path('cadastro/acoes/veiculo/', views.abordagem_veicular, name='veiculo'),
    path('cadastro/acoes/estabelecimento/', views.fiscalizacao_estabelecimento, name='estabelecimento'),
]