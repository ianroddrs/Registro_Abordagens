from django import forms
from .models import *

class OcorrenciasForm(forms.ModelForm):
    
    class Meta:
        model = ModelOcorrencias
        fields = ['nro_bop', 'apresentacao', 'enquadramento', 'fato_relevante',]

class PessoasForm(forms.ModelForm):
    nome_completo = forms.CharField(required=False, label='Nome completo')
    data_nascimento = forms.DateField(required=False,
        label='Data fim',
        widget=forms.DateInput(
            format='%d-%m-%Y',
            attrs={
                'type': 'date',
            }),
        input_formats=('%Y-%m-%d',),
    )
    class Meta:
        model = ModelPessoas
        fields = ['nome_completo', 'data_nascimento', 'genero', 'nro_documento','nome_mae','nome_pai','endereco_residencial']

class ApreensaoForm(forms.ModelForm):
    
    class Meta:
        model = ModelApreensao
        fields = ['endereco','tipo_objeto','tipo_droga','qtd_droga','und_medida','tipo_arma','especie_arma','qtd_arma','municao','imei1_celular','imei2_celular','outros_objetos','qtd_outros_objetos','placa_veiculo',]

class ProcedimentoForm(forms.ModelForm):
    
    class Meta:
        model = ModelProcedimento
        fields = ['nro_bop','nro_procedimento','apresentacao','enquadramento','fato_relevante',]