from django.db import models

class Usuarios(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True, unique=True, blank=False, null=False, editable=False)
    name = models.CharField(max_length=200, blank=False, null=False)
    instituicao = models.CharField(max_length=100, blank=False, null=False)
    funcional = models.IntegerField(blank=False, null=False)
    chefe = models.BooleanField(blank=False, null=False)
    
class pessoa(models.Model):
    nome = models.CharField(max_length=200, blank=False, null=False)
    data_nascimento = models.DateField(null=False, blank=False)
    cpf = models.IntegerField(null=False, blank=False, primary_key=True)
    mae = models.CharField(max_length=200,blank=False, null=False)
    
class registro(models.Model):
    nro_registro = models.CharField(max_length=100,null=False,blank=False, primary_key=True,auto_created=True)
    data_registro = models.DateTimeField(null=False,blank=False, auto_now_add=True)
    tipo_servico = models.CharField(max_length=200,null=False,blank=False)
    id_usuario_registro = models.ForeignKey("pessoa",on_delete=models.CASCADE)
    data_manutencao = models.DateTimeField(null=False,blank=False, auto_now=True)
    chefe_guarnicao = models.CharField(max_length=200,null=False,blank=False)
    
    