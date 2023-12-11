from django import forms
from .models import *

class OcorrenciasForm(forms.ModelForm):
    nro_bop = forms.CharField(required=True, label='Nro Bop')
    apresentacao = forms.BooleanField(required=False, label='Apresentação', widget=forms.CheckboxInput())
    enquadramento = forms.CharField(required=True, label='Enquadramento')
    fato_relevante = forms.BooleanField(required=False, label='Fato Relevante', widget=forms.CheckboxInput())
    cumprimento_mediadas = forms.BooleanField(required=False, label='Cumprimento de Medidas', widget=forms.CheckboxInput())
    instituicao = forms.CharField(required=False, label='Instituição')
    processo = forms.CharField(required=False, label='Nro Processo')
    
    class Meta:
        model = ModelBop
        fields = ['nro_bop', 'apresentacao', 'enquadramento', 'fato_relevante','cumprimento_medidas','instituicao','processo',]

                  
class ApreensaoForm(forms.ModelForm):
    endereco = forms.CharField(required=False, label='Endereço Apreensão',widget=forms.TextInput(attrs={'class': 'form-control'}),)
    data_apreensao = forms.DateField(required=False,label='Data Apreensão',widget=forms.DateInput(format='%d-%m-%Y',attrs={'type': 'date','class': 'form-control'}),input_formats=('%Y-%m-%d',),)
    objeto_apreendido = forms.ChoiceField(required=False,widget=forms.Select(attrs={'class': 'form-select obj-apreendido d-none', 'onchange':'toggleCampos()'}),choices=CLASS_OBJ,label='',)
    tipo_objeto = forms.CharField(required=False, label="Tipo Objeto",widget=forms.TextInput(attrs={'class':'form-control'}),)
    especie_modelo = forms.CharField(required=False, label='Especie/Modelo',widget=forms.TextInput(attrs={'class':'form-control campos-form'}))
    nro_identificador = forms.CharField(required=False, label="Nº Identificador",widget=forms.TextInput(attrs={'class':'form-control campos-form'}))
    tipo_nro_identificador = forms.CharField(required=False, label='Tipo Nº Identificador',widget=forms.TextInput(attrs={'class':'form-control campos-form'}))
    nro_identificador2 = forms.CharField(required=False, label="Nº Identificador2",widget=forms.TextInput(attrs={'class':'form-control campos-form'}))
    tipo_nro_identificador2 = forms.CharField(required=False,label='Tipo Nº Identificador2',widget=forms.TextInput(attrs={'class':'form-control campos-form'}))
    qtd = forms.FloatField(required=False, label='QTD',widget=forms.NumberInput(attrs={'class':'form-control'}))
    und_medida = forms.ChoiceField(required=False,widget=forms.Select(attrs={'class':'form-select'}),choices=UNIDADE_MEDIDA,label='Unidade de Medida')
    
    class Meta:
        model = ModelApreensao
        fields = ['endereco','data_apreensao','objeto_apreendido','tipo_objeto','especie_modelo','nro_identificador','tipo_nro_identificador','nro_identificador2','tipo_nro_identificador2','qtd','und_medida',]

class ProcedimentoForm(forms.ModelForm):
    class Meta:
        model = ModelProcedimento
        fields = ['nro_procedimento','enquadramento',]

class BopProcForm(forms.ModelForm):
    
    class Meta:
        model = ModelBop_Procedimento
        fields = ['nro_bop','nro_procedimento']