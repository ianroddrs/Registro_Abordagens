from django import forms
from .models import *
from mainApp.list_choices import TP_DROGA

class RegistrosPCEPAForm(forms.ModelForm):
    protocolo = forms.CharField(required=True, label='Protocolo',widget=forms.TextInput(attrs={'placeholder': 'Digite o protocolo','class': 'form-control'}),)
    caso = forms.CharField(required=True, label='Caso',widget=forms.TextInput(attrs={'placeholder': 'Digite o caso','class': 'form-control'}),)
    bop_tombo = forms.CharField(required=True, label='Bop/Tombo',widget=forms.TextInput(attrs={'class': 'form-control'}),)
    tipo_exame = forms.CharField(required=True, label='Tipo Exame',widget=forms.TextInput(attrs={'class': 'form-control'}),)
    data_exame = forms.DateField(required=True,label='Data Exame',widget=forms.DateInput(format='%d-%m-%Y',attrs={'type': 'date','class': 'form-control'}),input_formats=('%Y-%m-%d',),)
    
    
    class Meta:
        model = ModelRegistrospcepa
        fields = ['protocolo','caso','bop_tombo','tipo_exame','data_exame',]

class AnaliseDrogaForm(forms.ModelForm):
    tipo_droga = forms.ChoiceField(required=True,widget=forms.Select(attrs={'class': 'form-select'}),choices=TP_DROGA,label='Tipo Droga',initial=None)
    apresentacao = forms.BooleanField(required=False, label='Apresentação', widget=forms.CheckboxInput())
    qtd = forms.FloatField(required=True, label='QTD',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'EX: 1,5'}))
    und_medida = forms.ChoiceField(required=True,widget=forms.Select(attrs={'class':'form-select'}),choices=UNIDADE_MEDIDA,label='Unidade de Medida')
    
    class Meta:
        model = ModelAnaliseDrogapcepa
        fields = ['tipo_droga', 'apresentacao', 'qtd', 'und_medida',]

class AnaliseBalisticaForm(forms.ModelForm):
    tipo_material = forms.CharField(required=True,label='Tipo Material',widget=forms.TextInput(attrs={'class':'form-control'}))
    calibre = forms.FloatField(required=True,label='Calibre',widget=forms.TextInput(attrs={'class':'form-control'}))
    nro_serie_rastreio = forms.CharField(required=True,label='Nº Serie/Rastreio', widget=forms.TextInput(attrs={'class':'form-control'}))
    nro_patrimonio = forms.CharField(required=True,label='Nº Patrimonio',widget=forms.TextInput(attrs={'class':'form-control'}))
    qtd = forms.FloatField(required=True, label='QTD',widget=forms.TextInput(attrs={'class':'form-control'}))
    
    class Meta:
        model = ModelAnaliseBalisticapcepa
        fields = ['tipo_material','calibre','nro_serie_rastreio','nro_patrimonio','qtd']
        
