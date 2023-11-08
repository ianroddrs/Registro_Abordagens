from django.db import models
from mainApp.models import *
from pc.models import *
# Create your models here.
# alterar


    
class ModelAnaliseDrogapcepa(models.Model):
    protocolo = models.AutoField(primary_key=True, unique=True, db_index=True, serialize=True)
    tipo_droga = models.CharField(max_length=100,null=False,blank=False,choices=TP_DROGA)
    aprensentacao = models.BooleanField(null=False,blank=False)
    qtd = models.FloatField(null=False,blank=False)
    und_medida = models.CharField(max_length=20,null=False,blank=False,choices=UNIDADE_MEDIDA)
    id_imagem = models.ForeignKey(ModelImagens, db_column='id_imagem', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'pcepa_analise_droga'
    
    
class ModelAnaliseBalisticapcepa(models.Model):
    protocolo = models.AutoField(primary_key=True, unique=True, db_index=True, serialize=True)
    tipo_material = models.CharField(max_length=100,null=False,blank=False)
    calibre = models.CharField(max_length=20,null=False,blank=False)
    nro_serie_rastreio = models.CharField(max_length=50,null=False,blank=False)
    nro_patrimonio = models.CharField(max_length=50,null=True,blank=False)
    qtd = models.IntegerField(null=False,blank=False)
    id_imagem = models.ForeignKey(ModelImagens, db_column='id_imagem', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'pcepa_analise_balistica'
    
class ModelPericiaVeicularpcepa(models.Model):
    protocolo = models.AutoField(primary_key=True, unique=True, db_index=True, serialize=True)
    foto_veiculo = models.CharField(max_length=999**999,null=False,blank=False)
    foto_placa = models.CharField(max_length=999**999,null=False,blank=False)
    
    class Meta:
        db_table = 'pcepa_pericia_veicular'
    
class ModelLesaoCorporalpcepa(models.Model):
    protocolo = models.AutoField(primary_key=True, unique=True, db_index=True, serialize=True)
    nro_documento = models.CharField(max_length=100,null=False,blank=False)
    foto_documento = models.CharField(max_length=999**999,null=False,blank=False)
    
    class Meta:
        db_table = 'pcepa_lesao_corporal'
    
class ModelLocalCrimepcepa(models.Model):
    protocolo = models.AutoField(primary_key=True, unique=True, db_index=True, serialize=True)
    latitude = models.CharField(max_length=100,null=False,blank=False)
    longitude = models.CharField(max_length=100,null=False,blank=False)
    preservacao_local = models.CharField(max_length=100,null=False,blank=False)
    vestigios_coletados = models.CharField(max_length=100,null=False,blank=False)
    nro_doc_identficacao = models.CharField(max_length=100,null=False,blank=False)
    foto_doc_identificacao = models.CharField(max_length=999**999,null=False,blank=False)
    
    class Meta:
        db_table = 'pcepa_local_crime'
    
class ModelNecropsiaRemocaopcepa(models.Model):
    protocolo = models.AutoField(primary_key=True, unique=True, db_index=True, serialize=True)
    nro_doc_identficacao = models.CharField(max_length=100,null=False,blank=False)
    foto_doc_identificacao = models.CharField(max_length=999**999,null=False,blank=False)
    causa_provavel_morte = models.CharField(max_length=100,null=False,blank=False)
    
    class Meta:
        db_table = 'pcepa_necropsia_remocao'
    
    
class ModelRegistrospcepa(models.Model):
    protocolo = models.CharField(primary_key=True,max_length=30,null=False,blank=False)
    caso = models.CharField(max_length=50,null=False,blank=False)
    bop_tombo = models.CharField(max_length=100,null=False,blank=False)
    tipo_exame = models.CharField(max_length=100,null=False,blank=False)
    data_exame = models.DateTimeField(auto_now=False, auto_now_add=False)
    id_envolvido = models.ForeignKey(ModelPessoas, db_column='id_envolvido',related_name='id_envolvido_pcepa',on_delete=models.CASCADE)
    data_registro = models.DateTimeField(auto_now_add=True)
    data_manutencao = models.DateTimeField(auto_now=True)
    id_usuario = models.ForeignKey(ModelUsuarios, db_column='id_usuario',related_name='id_usuario_pcepa',on_delete=models.CASCADE)
    id_operacao = models.ForeignKey(ModelOperacoes, db_column='id_operacao',related_name='id_operacao_pcepa', on_delete=models.CASCADE)
    id_analise_balistica = models.ForeignKey(ModelAnaliseBalisticapcepa, db_column='id_analise_balistica', on_delete=models.CASCADE)
    id_pericia_veicular = models.ForeignKey(ModelPericiaVeicularpcepa, db_column='id_pericia_veicular', on_delete=models.CASCADE)
    id_lesao_corporal = models.ForeignKey(ModelLesaoCorporalpcepa, db_column='id_lesao_corporal', on_delete=models.CASCADE)
    id_local_crime = models.ForeignKey(ModelLocalCrimepcepa, db_column='id_local_crime', on_delete=models.CASCADE)
    id_necropsia_remocao = models.ForeignKey(ModelNecropsiaRemocaopcepa, db_column='id_necropsia_remocao', on_delete=models.CASCADE)
    id_analise_droga = models.ForeignKey(ModelAnaliseDrogapcepa, db_column='id_analise_droga', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'pcepa_registros'