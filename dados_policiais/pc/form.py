from django import forms
from .models import *

class OcorrenciasForm(forms.ModelForm):
    
    class Meta:
        model = ModelOcorrencias
        fields = ['nro_bop', 'apresentacao', 'enquadramento', 'fato_relevante',]

class PessoasForm(forms.ModelForm):
    id_pessoa = forms.IntegerField(required=False,widget=forms.HiddenInput())
    nome_completo = forms.CharField(required=False, label='Nome completo')
    data_nascimento = forms.DateField(required=False,label='Data nascimento',widget=forms.DateInput(format='%d-%m-%Y',attrs={'type': 'date',}),input_formats=('%Y-%m-%d',),)
    genero = forms.ChoiceField(required=False,widget=forms.Select,choices=GENERO,)
    nro_documento = forms.IntegerField(required=False,)
    nome_mae = forms.CharField(required=False, label='Nome da mae')
    nome_pai = forms.CharField(required=False, label='Nome do pai')
    endereco_residencial = forms.CharField(required=False, label='Endereco residencial')
    
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