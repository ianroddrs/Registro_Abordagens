from django.db import models
from mainApp.models import *
from pc.models import *
# Create your models here.
# alterar


class ModelRegistrospcepa(models.Model):
    protocolo = models.CharField(primary_key=True,max_length=30,null=False,blank=False)
    caso = models.CharField(max_length=50,null=False,blank=False)
    bop_tombo = models.CharField(max_length=100,null=False,blank=False)
    tipo_exame = models.CharField(max_length=100,null=False,blank=False)
    data_exame = models.DateTimeField(auto_now=False, auto_now_add=False)
    data_registro = models.DateTimeField(auto_now_add=True)
    data_manutencao = models.DateTimeField(auto_now=True)
    id_usuario = models.ForeignKey(ModelUsuarios, db_column='id_usuario',related_name='id_usuario_pcepa',on_delete=models.CASCADE)
    id_operacao = models.ForeignKey(ModelOperacoes, db_column='id_operacao',related_name='id_operacao_pcepa', on_delete=models.CASCADE)
    id_comandante = models.ForeignKey(ModelUsuarios, db_column='id_comandante',related_name='id_comandante_pcepa', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'pcepa_registros'
    
class ModelAnaliseDrogapcepa(models.Model):
    protocolo = models.ForeignKey(ModelRegistrospcepa, db_column='protocolo',related_name='protocolo_droga_pcepa', on_delete=models.CASCADE)
    tipo_droga = models.CharField(max_length=100,null=False,blank=False,choices=TP_DROGA)
    apresentacao = models.BooleanField(null=True,blank=False)
    qtd = models.FloatField(null=False,blank=False)
    und_medida = models.CharField(max_length=20,null=False,blank=False,choices=UNIDADE_MEDIDA)
    id_imagem = models.ForeignKey(ModelImagens, db_column='id_imagem', on_delete=models.CASCADE,null=True,blank=False, default=None)
    
    class Meta:
        db_table = 'pcepa_analise_droga'
    
    
class ModelAnaliseBalisticapcepa(models.Model):
    protocolo = models.ForeignKey(ModelRegistrospcepa, db_column='protocolo',related_name='protocolo_balistica_pcepa', on_delete=models.CASCADE)
    tipo_material = models.CharField(max_length=100,null=False,blank=False)
    calibre = models.CharField(max_length=20,null=False,blank=False)
    nro_serie_rastreio = models.CharField(max_length=50,null=False,blank=False)
    nro_patrimonio = models.CharField(max_length=50,null=True,blank=False)
    qtd = models.IntegerField(null=False,blank=False)
    
    class Meta:
        db_table = 'pcepa_analise_balistica'
    
class ModelPericiaVeicularpcepa(models.Model):
    protocolo = models.ForeignKey(ModelRegistrospcepa, db_column='protocolo',related_name='protocolo_veiculo_pcepa', on_delete=models.CASCADE)
    id_veiculo = models.ForeignKey(ModelVeiculos, db_column='id_veiculo',related_name='id_veiculo_pcepa', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'pcepa_pericia_veicular'
    
class ModelLesaoCorporalpcepa(models.Model):
    protocolo = models.ForeignKey(ModelRegistrospcepa, db_column='protocolo',related_name='protocolo_lesao_pcepa', on_delete=models.CASCADE)
    id_pessoa = models.ForeignKey(ModelPessoas, db_column='id_pessoa',related_name='id_pessoa_lesao_pcepa', on_delete=models.CASCADE)
        
    class Meta:
        db_table = 'pcepa_lesao_corporal'
    
class ModelLocalCrimepcepa(models.Model):
    protocolo = models.ForeignKey(ModelRegistrospcepa, db_column='protocolo',related_name='protocolo_local_pcepa', on_delete=models.CASCADE)
    latitude = models.CharField(max_length=100,null=False,blank=False)
    longitude = models.CharField(max_length=100,null=False,blank=False)
    preservacao_local = models.CharField(max_length=100,null=False,blank=False)
    vestigios_coletados = models.CharField(max_length=100,null=False,blank=False)
    nro_doc_identficacao = models.CharField(max_length=100,null=False,blank=False)

    
    class Meta:
        db_table = 'pcepa_local_crime'
    
class ModelNecropsiaRemocaopcepa(models.Model):
    protocolo = models.ForeignKey(ModelRegistrospcepa, db_column='protocolo',related_name='protocolo_necropsia_pcepa', on_delete=models.CASCADE)
    nro_doc_identficacao = models.CharField(max_length=100,null=False,blank=False)
    causa_provavel_morte = models.CharField(max_length=100,null=False,blank=False)
    
    class Meta:
        db_table = 'pcepa_necropsia_remocao'
    
    
class ModelRegistrosPessoaspcepa(models.Model):
    protocolo = models.ForeignKey(ModelRegistrospcepa, db_column='protocolo',related_name='protocolo_pessosas_pcepa', on_delete=models.CASCADE)
    id_pessoa = models.ForeignKey(ModelPessoas, db_column='id_pessoa',related_name='id_pessoa_pcepa',on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'pcepa_registros_pessoas'
        
class ModelRegistrosImagens(models.Model):
    protocolo = models.ForeignKey(ModelRegistrospcepa, db_column='protocolo',related_name='protocolo_imagem_pcepa', on_delete=models.CASCADE)
    id_imagem = models.ForeignKey(ModelImagens, db_column='id_imagem',related_name='id_imagem_pcepa',on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'pcepa_registros_imagens'