from django import forms
from .models import *
from mainApp.list_choices import *

class ImagemForm(forms.ModelForm):
    imagem = forms.FileField(required=True, label='Imagem',widget=forms.FileInput(attrs={'class':'form-control','accept':'image/*','capture':'camera'}))
    
    class Meta:
        model = ModelImagens
        fields = ['imagem',]

class PessoasForm(forms.ModelForm):
    pj = forms.BooleanField(required=False, label='Pessoa Juridica', widget=forms.CheckboxInput(attrs={'class':'form-check-input'},check_test=lambda x: False), initial='True',label_suffix='')
    id_pessoa = forms.IntegerField(required=False,widget=forms.HiddenInput())
    nome_completo = forms.CharField(required=True, label="Nome completo", widget=forms.TextInput(attrs={'class':'form-control'}))
    data_nascimento = forms.DateField(required=True,label='Data nascimento',widget=forms.DateInput(format='%d-%m-%Y',attrs={'type': 'date','class': 'form-control'}),input_formats=('%Y-%m-%d',),)
    genero = forms.ChoiceField(required=True,choices=GENERO,widget=forms.Select(attrs={'class':'form-select'}))
    nro_documento = forms.IntegerField(required=True,widget=forms.TextInput(attrs={'class':'form-control', 'mask':'number'}))
    nome_mae = forms.CharField(required=True, label='Nome da mae', widget=forms.TextInput(attrs={'class':'form-control'}))
    nome_pai = forms.CharField(required=False, label='Nome do pai', widget=forms.TextInput(attrs={'class':'form-control'}))
    endereco = forms.CharField(required=False, label='Endereço', widget=forms.TextInput(attrs={'class':'form-control'}))
    atuacao = forms.ChoiceField(required=True,widget=forms.HiddenInput(),choices=ATUACAO,initial='RELATOR')
    
    class Meta:
        model = ModelPessoas
        fields = ['pj','nome_completo', 'data_nascimento', 'genero', 'nro_documento','nome_mae','nome_pai','endereco']