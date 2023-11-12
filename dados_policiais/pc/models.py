from django.db import models
from mainApp.models import *

INST = (
    ('PM','PM'),
    ('PC','PC'),
    ('PC/PM','PC/PM'),
)
UNIDADE_MEDIDA = (
    ('Kg','QUILOGRAMA'),
    ('g','GRAMAS'),
    ('UND','UNIDADE'),
    ('L','LITROS'),
)

TP_OBJ = (
    ('DOCUMENTO','DOCUMENTO'),
    ('CELULAR','CELULAR'),
    ('OUTRO','OUTRO OBJETO'),
    ('ARMA','ARMA'),
    ('MUNICAO','MUNICAO'),
    ('DROGA','DROGA'),
    ('RECURSO_NATURAL','RECURSO NATURAL'),
    ('PARTES_DO_CORPO','PARTES DO CORPO'),
    ('VEICULO','VEICULO'),
)

TP_DROGA = (
    ('ANFETAMINA','ANFETAMINA'),('COCAINA','COCAINA'),('CRACK','CRACK'),('ECSTASY','ECSTASY'),
    ('MACONHA','MACONHA'),('MDMA','MDMA'),('MERLA','MERLA'),('NOBESIO','NOBESIO'),
    ('OXI','OXI'),
)

TP_ARMA = (
    ('ARMA_DE_FOGO','ARMA DE FOGO'),
    ('ARMA_BRANCA','ARMA BRANCA'),
    ('SIMULACRO','SIMULACRO'),
)


# Create your models here.
class ModelOcorrencias(models.Model):
    nro_bop = models.CharField(max_length=100, primary_key=True, null=False, blank=False)
    data_registro = models.DateTimeField(auto_now_add=True)
    data_manutencao = models.DateTimeField(auto_now=True)
    apresentacao = models.BooleanField(null=False)
    cumprimento_medidas = models.BooleanField(null=False)
    instituicao = models.CharField(max_length=10, null=True, blank=False,choices=INST)
    processo = models.CharField(max_length=100,null=True,blank=False)
    enquadramento = models.CharField(max_length=200, null=False, blank=False)
    fato_relevante = models.BooleanField(null=False)
    id_relator = models.ForeignKey(ModelPessoas, db_column='id_relator',related_name='id_relator',on_delete=models.CASCADE)
    id_suspeito = models.ForeignKey(ModelPessoas, db_column='id_suspeito',related_name='id_suspeito',on_delete=models.CASCADE)
    id_usuario = models.ForeignKey(ModelUsuarios, db_column='id_usuario',related_name='id_usuario_pc_ocor',on_delete=models.CASCADE)
    id_comandante = models.ForeignKey(ModelUsuarios, db_column='id_comandante',related_name='id_comandante_pc_ocor', on_delete=models.CASCADE)
    id_operacao = models.ForeignKey(ModelOperacoes, db_column='id_operacao',related_name='id_operacao_pc_ocor', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'pc_ocorrencias'


class ModelProcedimento(models.Model):
    nro_procedimento = models.CharField(max_length=100, primary_key=True, null=False, blank=False)
    data_registro = models.DateTimeField(auto_now_add=True)
    data_manutencao = models.DateTimeField(auto_now=True)
    apresentacao = models.BooleanField(null=False)
    enquadramento = models.CharField(max_length=200, null=False, blank=False)
    fato_relevante = models.BooleanField(null=False)
    id_apresentante = models.ForeignKey(ModelPessoas, db_column='id_apresentante',on_delete=models.CASCADE)
    id_autor = models.ForeignKey(ModelPessoas, db_column='id_autor',related_name='id_autor_pc',on_delete=models.CASCADE)
    id_usuario = models.ForeignKey(ModelUsuarios, db_column='id_usuario',related_name='id_usuario_pc_proced',on_delete=models.CASCADE)
    id_comandante = models.ForeignKey(ModelUsuarios, db_column='id_comandante',related_name='id_comandante_pc_proced', on_delete=models.CASCADE)
    id_operacao = models.ForeignKey(ModelOperacoes, db_column='id_operacao',related_name='id_operacao_pc_proced', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'pc_procedimentos'

class ModelBop_Procedimento(models.Model):
    nro_bop = models.ForeignKey(ModelOcorrencias,db_column='nro_bop',related_name='nro_bop_pc_proced', on_delete=models.CASCADE)
    nro_procedimento = models.ForeignKey(ModelProcedimento,db_column='nro_procedimento',related_name='nro_procedimento_pc_proced', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'pc_bop_proc'
        
class ModelApreensao(models.Model):
    id_apreensao = models.AutoField(primary_key=True, unique=True, db_index=True, serialize=True)
    endereco = models.CharField(max_length=200, null=False, blank=False)
    tipo_objeto = models.CharField(max_length=200, choices=TP_OBJ)
    tipo_droga = models.CharField(max_length=200, choices=TP_DROGA)
    qtd_droga = models.FloatField(null=False, blank=False)
    und_medida = models.CharField(max_length=200, choices=UNIDADE_MEDIDA)
    tipo_arma = models.CharField(max_length=200, choices=TP_ARMA)
    especie_arma = models.CharField(max_length=50, null=False, blank=False)
    qtd_arma = models.IntegerField(null=False, blank=False)
    municao = models.IntegerField(null=False, blank=False)
    imei1_celular = models.CharField(max_length=50, null=False, blank=False)
    imei2_celular = models.CharField(max_length=50, null=False, blank=False)
    outros_objetos = models.CharField(max_length=200, null=False, blank=False)
    qtd_outros_objetos = models.IntegerField(null=False, blank=False)
    placa_veiculo = models.CharField(max_length=20, null=False, blank=False)
    data_registro = models.DateTimeField(auto_now_add=True)
    data_manutencao = models.DateTimeField(auto_now=True)
    # fato_relevante = models.BooleanField(null=False)
    # id_usuario = models.ForeignKey(ModelUsuarios, db_column='id_usuario',related_name='id_usuario_pc_apre',on_delete=models.CASCADE)
    # id_operacao = models.ForeignKey(ModelOperacoes, db_column='id_operacao',related_name='id_operacao_pc_apre', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'pc_apreensao'

class ModelOcorrencia_Apreensao(models.Model):
    nro_bop = models.ForeignKey(ModelOcorrencias,db_column='nro_bop',related_name='nro_bop_apreensao', on_delete=models.CASCADE,null=True)
    id_apreensao = models.ForeignKey(ModelOcorrencias,db_column='id_apreensao',related_name='id_apreensao_apreensao', on_delete=models.CASCADE,null=True) #foreignkey ocorrencia
    
    class Meta:
        db_table = 'pc_ocorrencia_apreensao'
        
class ModelCumprimentoMedidas(models.Model):
    nro_bop = models.ForeignKey(ModelOcorrencias,db_column='nro_bop',related_name='nro_bop_pc_CM', on_delete=models.CASCADE)
    processo = models.CharField(max_length=100,null=False,blank=False)
    enquadramento = models.CharField(max_length=200, null=False, blank=False)
    instituicao = models.CharField(max_length=10, null=False, blank=False,choices=INST)
    data_registro = models.DateTimeField(auto_now_add=True)
    data_manutencao = models.DateTimeField(auto_now=True)
    fato_relevante = models.BooleanField(null=False)
    id_usuario = models.ForeignKey(ModelUsuarios, db_column='id_usuario',related_name='id_usuario_pc_cump',on_delete=models.CASCADE)
    id_operacao = models.ForeignKey(ModelOperacoes, db_column='id_operacao',related_name='id_operacao_pc_cump', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'pc_cumprimento_medidas'