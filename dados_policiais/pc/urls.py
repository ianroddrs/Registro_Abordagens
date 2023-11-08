from django.urls import path
from . import views

urlpatterns = [
    path('cadastro/acoes/nro_ocorrencia/', views.nro_ocorrencia, name='nro_ocorrencia'),
    path('cadastro/acoes/proced_policial/', views.proced_policial, name='proced_policial'),
    path('cadastro/acoes/apreensao/', views.apreensao, name='apreensao'),
    path('cadastro/acoes/cumprimento_medidas_cautelares/', views.cumprimento_medidas_cautelares, name='cumprimento_medidas_cautelares'),
]