from django.urls import path
from . import views

urlpatterns = [
    path('cadastro/acoes/analise_droga/', views.analise_droga, name='analise_droga'),
    path('cadastro/acoes/analise_balistica/', views.analise_balistica, name='analise_balistica'),
    path('cadastro/acoes/pericia_veicular/', views.pericia_veicular, name='pericia_veicular'),
]