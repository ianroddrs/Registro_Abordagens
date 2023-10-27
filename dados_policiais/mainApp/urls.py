from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name="login"),
    path('sair/', views.sair, name='sair'),
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('registros/', views.registros, name='registros'),
    path('registros/<int:id>/', views.view_registro, name='view_registro'),
    path('operacoes/', views.operacoes, name='operacoes'),
    path('cadastro/usuario/', views.usuario, name='usuario'),
    path('cadastro/operacao/', views.cad_operacao, name='cad_operacao'),
    path('cadastro/acoes/', views.acoes, name='acoes'),
    path('cadastro/acoes/abordagem/', views.cad_abordagem, name='cad_abordagem'),
    path('cadastro/acoes/veiculo/', views.abordagem_veicular, name='veiculo'),
    path('cadastro/acoes/estabelecimento/', views.fiscalizacao_estabelecimento, name='estabelecimento'),
    path('cadastro/acoes/busca_apreensao/', views.busca_apreensao, name='busca_apreensao'),
]