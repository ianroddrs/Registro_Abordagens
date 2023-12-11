from django.urls import path
from . import views

urlpatterns = [
    path('cadastro/acoes/nro_ocorrencia/', views.nro_ocorrencia, name='nro_ocorrencia'),
    path('cadastro/acoes/proced_policial/', views.proced_policial, name='proced_policial'),
    path('registros/ocorrencias/', views.pc_ocorrencias, name='ocorrencias'),
]