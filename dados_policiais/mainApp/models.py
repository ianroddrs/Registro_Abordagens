from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from .list_choices import *


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    first_name = models.CharField(max_length=150)
    
    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    action_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'

class ModelImagens(models.Model):
    id_imagem = models.AutoField(primary_key=True, unique=True, db_index=True, serialize=True)
    imagem = models.TextField(max_length=999**999,null=False,blank=False)
    
    class Meta:
        db_table = 'imagens'
 
class ModelUsuarios(models.Model):
    # id = models.AutoField(primary_key=True, unique=True, db_index=True, serialize=True)
    nome_completo = models.CharField(max_length=200, blank=False, null=False)
    instituicao = models.CharField(max_length=100, blank=False, null=False)
    funcional = models.IntegerField(blank=False, null=False)
    comandante = models.BooleanField(blank=False, null=False)
    data_registro = models.DateTimeField(auto_now_add=True)
    data_manutencao = models.DateTimeField(auto_now=True)
    id = models.OneToOneField(User, db_column='id',on_delete=models.CASCADE,primary_key=True)
    
    class Meta:
        db_table = 'usuarios'

class ModelOperacoes(models.Model):
    nome_operacao = models.CharField(max_length=200, blank=False, null=False)
    data_inicio = models.DateTimeField(null=False, blank=False)
    data_fim = models.DateTimeField(null=True)
    responsavel = models.CharField(max_length=200,blank=False, null=False)
    data_registro = models.DateTimeField(auto_now_add=True)
    data_manutencao = models.DateTimeField(auto_now=True)
        
    class Meta:
        db_table = 'operacoes'


class ModelPessoas(models.Model):
    pj = models.BooleanField(null=False)
    id_pessoa = models.AutoField(primary_key=True,unique=True, db_index=True, serialize=True,null=False,blank=False)
    nome_completo = models.CharField(max_length=200, blank=False, null=False)
    data_nascimento = models.DateField(null=False, blank=False)
    genero = models.CharField(max_length=10, null=False, blank=False,choices=GENERO)
    nro_documento = models.IntegerField(null=False, blank=False)
    nome_mae = models.CharField(max_length=200,blank=False, null=False)
    nome_pai = models.CharField(max_length=200,blank=False, null=True)
    endereco = models.CharField(max_length=100,null=True,blank=False)
    data_registro = models.DateTimeField(auto_now_add=True)
    data_manutencao = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'pessoas'
        

class ModelVeiculos(models.Model):
    id_veiculo = models.AutoField(primary_key=True,unique=True, db_index=True, serialize=True,null=False,blank=False)
    tipo_veiculo = models.CharField(max_length=200, blank=False, null=False)
    marca = models.CharField(max_length=100,null=True,blank=False)
    modelo = models.CharField(max_length=100,null=True,blank=False)
    placa = models.CharField(max_length=20,null=False,blank=False)
    renavam = models.CharField(max_length=100,null=True,blank=False)
    niv_chassi = models.CharField(max_length=100,null=True,blank=False)
    niv_chassi_revelado = models.CharField(max_length=100,null=True,blank=False)
    proprietario = models.CharField(max_length=200,blank=False, null=False)
    irregularidade = models.CharField(max_length=200,blank=False, null=True)
    veiculo_apreendido = models.BooleanField(null=True)
    data_registro = models.DateTimeField(auto_now_add=True)
    data_manutencao = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'veiculos'
        
class ModelEstabelecimentos(models.Model):
    id_estabelecimento = models.AutoField(primary_key=True,unique=True, db_index=True, serialize=True,null=False,blank=False)
    tipo_estabelecimento = models.CharField(max_length=200, blank=False, null=False)
    endereco = models.CharField(max_length=200,blank=False, null=False)
    proprietario = models.CharField(max_length=200,blank=False, null=False)
    irregularidade = models.CharField(max_length=200,blank=False, null=False)
    estabelecimento_interditado = models.BooleanField()
    data_registro = models.DateTimeField(auto_now_add=True)
    data_manutencao = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'estabelecimento'
        
class ModelRegistrosAbordagem(models.Model):
    nro_registro = models.AutoField(primary_key=True, unique=True, db_index=True, serialize=True)
    data_registro = models.DateTimeField(auto_now_add=True)
    id_usuario = models.ForeignKey(ModelUsuarios, db_column='id_usuario',related_name='id_usuario',on_delete=models.CASCADE)
    data_manutencao = models.DateTimeField(auto_now=True)
    comandante = models.IntegerField(null=False,blank=False)
    id_operacao = models.ForeignKey(ModelOperacoes, db_column='id_operacao',related_name='id_operacao', on_delete=models.CASCADE)
    id_envolvido = models.ForeignKey(ModelPessoas,db_column='id_envolvido',related_name='id_envolvido_pm',on_delete=models.CASCADE,null=True,blank=False)
    id_veiculo = models.ForeignKey(ModelVeiculos,db_column='id_veiculo',related_name='id_reg_veiculo',on_delete=models.CASCADE,null=True,blank=False)
    id_condutor_veiculo = models.ForeignKey(ModelPessoas,db_column='id_condutor_veiculo',related_name='id_condutor_veiculo',on_delete=models.CASCADE,null=True,blank=False)
    id_estabelecimento = models.ForeignKey(ModelEstabelecimentos,db_column='id_estabelecimento',related_name='id_reg_estabelecimento',on_delete=models.CASCADE,null=True,blank=False)
    id_foto_abordado = models.ForeignKey(ModelImagens,db_column='id_foto_abordado',related_name='id_foto_abordado',on_delete=models.CASCADE,null=True,blank=False)
    id_foto_documento = models.ForeignKey(ModelImagens,db_column='id_foto_documento',related_name='id_foto_documento',on_delete=models.CASCADE,null=True,blank=False)
    
    def __str__(self):
        return f"Registro {self.nro_registro}"

    class Meta:
        db_table = 'registros_abordagem'

class ModelIndicadores(models.Model):
    id = models.AutoField(primary_key=True, unique=True, db_index=True, serialize=True,null=False,blank=False)
    indicador = models.CharField(max_length=200, null=False, blank=False)
    instituicao = models.CharField(max_length=10, null=False, blank=False)
    icon = models.CharField(max_length=50, null=False, blank=False)
    endereco = models.CharField(max_length=50, null=False, blank=False)
    
    class Meta:
        db_table = 'indicadores'