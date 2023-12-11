from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name="login"),
    path('sair/', views.sair, name='sair'),
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('registros/acoes/', views.registro_acoes, name='registro_acoes'),
    path('registros/acoes/<int:id>/', views.registro_acao, name='registro_acao'),
    path('registros/operacoes/', views.registro_operacoes, name='registro_operacoes'),
    path('cadastro/usuario/', views.usuario, name='usuario'),
    path('cadastro/operacao/', views.cad_operacao, name='cad_operacao'),
    path('cadastro/acoes/', views.indicadores, name='indicadores'),
    path('API/pesquisa/', views.pesquisa_ajax, name='pesquisa_ajax'),
    path('extrato/', views.extrato, name='extrato'),
]