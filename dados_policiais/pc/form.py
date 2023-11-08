from django import forms
from .models import *

class OcorrenciasForm(forms.ModelForm):
    
    class Meta:
        model = ModelOcorrencias
        fields = ['nro_bop', 'apresentacao', 'enquadramento', 'fato_relevante',]

class PessoasForm(forms.ModelForm):
    
    class Meta:
        model = ModelPessoas
        fields = ['nome_completo', 'data_nascimento', 'genero', 'nro_documento','nome_mae','nome_pai','endereco_residencial']
