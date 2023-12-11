from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('cadastro/acoes/abordagem/', views.cad_abordagem, name='cad_abordagem'),
    path('cadastro/acoes/veiculo/', views.abordagem_veicular, name='veiculo'),
    path('cadastro/acoes/estabelecimento/', views.fiscalizacao_estabelecimento, name='estabelecimento'),
]