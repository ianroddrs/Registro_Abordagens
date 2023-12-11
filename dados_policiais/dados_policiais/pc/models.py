from django.db import models
from mainApp.models import *
from mainApp.list_choices import *



# Create your models here.
class ModelBop_Atuacao(models.Model):
    id_atuacao = models.AutoField(primary_key=True, unique=True, db_index=True, serialize=True)
    ds_atuacao = models.CharField(max_length=30, null=True, blank=False,choices=BOP_ATU)
    data_registro = models.DateTimeField(auto_now_add=True)
    data_manutencao = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'pc_bop_atuacao'
        
class ModelProced_Atuacao(models.Model):
    id_atuacao = models.AutoField(primary_key=True, unique=True, db_index=True, serialize=True)
    ds_atuacao = models.CharField(max_length=30, null=True, blank=False,choices=PROC_ATU)
    data_registro = models.DateTimeField(auto_now_add=True)
    data_manutencao = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'pc_procedimento_atuacao'
        
class ModelBop(models.Model):
    nro_bop = models.CharField(max_length=100, primary_key=True, null=False, blank=False)
    data_registro = models.DateTimeField(auto_now_add=True)
    data_manutencao = models.DateTimeField(auto_now=True)
    apresentacao = models.BooleanField(null=False)
    cumprimento_medidas = models.BooleanField(null=False)
    instituicao = models.CharField(max_length=10, null=True, blank=False,choices=INST)
    processo = models.CharField(max_length=100,null=True,blank=False)
    enquadramento = models.CharField(max_length=200, null=False, blank=False)
    fato_relevante = models.BooleanField(null=False)
    # id_relator = models.ForeignKey(ModelPessoas, db_column='id_relator',related_name='id_relator',on_delete=models.CASCADE)
    # id_suspeito = models.ForeignKey(ModelPessoas, db_column='id_suspeito',related_name='id_suspeito',on_delete=models.CASCADE)
    id_usuario = models.ForeignKey(ModelUsuarios, db_column='id_usuario',related_name='id_usuario_pc_ocor',on_delete=models.CASCADE)
    id_comandante = models.ForeignKey(ModelUsuarios, db_column='id_comandante',related_name='id_comandante_pc_ocor', on_delete=models.CASCADE)
    id_operacao = models.ForeignKey(ModelOperacoes, db_column='id_operacao',related_name='id_operacao_pc_ocor', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'pc_bop'


class ModelProcedimento(models.Model):
    nro_procedimento = models.CharField(max_length=100, primary_key=True, null=False, blank=False)
    data_registro = models.DateTimeField(auto_now_add=True)
    data_manutencao = models.DateTimeField(auto_now=True)
    enquadramento = models.CharField(max_length=200, null=False, blank=False)
    id_usuario = models.ForeignKey(ModelUsuarios, db_column='id_usuario',related_name='id_usuario_pc_proced',on_delete=models.CASCADE)
    id_comandante = models.ForeignKey(ModelUsuarios, db_column='id_comandante',related_name='id_comandante_pc_proced', on_delete=models.CASCADE)
    id_operacao = models.ForeignKey(ModelOperacoes, db_column='id_operacao',related_name='id_operacao_pc_proced', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'pc_procedimentos'

class ModelBop_Procedimento(models.Model):
    nro_bop = models.ForeignKey(ModelBop,db_column='nro_bop',related_name='nro_bop_pc_proced', on_delete=models.CASCADE)
    nro_procedimento = models.ForeignKey(ModelProcedimento,db_column='nro_procedimento',related_name='nro_procedimento_pc_proced', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'pc_bop_proc'

class ModelBop_Pessoa(models.Model):
    id_atuacao = models.ForeignKey(ModelBop_Atuacao,db_column='id_atuacao',related_name='id_atuacao_pc_bp', on_delete=models.CASCADE)
    id_pessoa = models.ForeignKey(ModelPessoas,db_column='id_pessoa',related_name='id_pessoa_pc_bp', on_delete=models.CASCADE)
    nro_bop = models.ForeignKey(ModelBop,db_column='nro_bop',related_name='nro_bop_pc_bp', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'pc_bop_pessoa'
        
class ModelProc_Pessoa(models.Model):
    id_atuacao = models.ForeignKey(ModelProced_Atuacao,db_column='id_atuacao',related_name='id_atuacao_pc_pp', on_delete=models.CASCADE)
    id_pessoa = models.ForeignKey(ModelPessoas,db_column='id_pessoa',related_name='id_pessoa_pc_pp', on_delete=models.CASCADE)
    nro_procedimento = models.ForeignKey(ModelProcedimento,db_column='nro_procedimento',related_name='nro_procedimento_pc_pp', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'pc_procedimento_pessoa'

class ModelApreensao(models.Model):
    id_apreensao = models.AutoField(primary_key=True, unique=True, db_index=True, serialize=True)
    endereco = models.CharField(max_length=200, null=False, blank=False)
    data_apreensao = models.DateField(null=False, blank=False)
    objeto_apreendido = models.CharField(max_length=200, choices=CLASS_OBJ)
    tipo_objeto = models.CharField(max_length=200)
    especie_modelo = models.CharField(max_length=200)
    nro_identificador = models.CharField(max_length=200)
    tipo_nro_identificador = models.CharField(max_length=200)
    nro_identificador2 = models.CharField(max_length=200)
    tipo_nro_identificador2 = models.CharField(max_length=200)
    qtd = models.FloatField(null=False, blank=False)
    und_medida = models.CharField(max_length=200, choices=UNIDADE_MEDIDA)
    
    class Meta:
        db_table = 'pc_apreensao'

class ModelBop_Apreensao(models.Model):
    nro_bop = models.ForeignKey(ModelBop,db_column='nro_bop',related_name='nro_bop_apreensao', on_delete=models.CASCADE,null=True)
    id_apreensao = models.ForeignKey(ModelApreensao,db_column='id_apreensao',related_name='id_apreensao_apreensao', on_delete=models.CASCADE,null=True) #foreignkey ocorrencia
    
    class Meta:
        db_table = 'pc_bop_apreensao'
        
class ModelCumprimentoMedidas(models.Model):
    nro_bop = models.ForeignKey(ModelBop,db_column='nro_bop',related_name='nro_bop_pc_CM', on_delete=models.CASCADE)
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