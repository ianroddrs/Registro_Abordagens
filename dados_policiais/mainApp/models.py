from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

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
        
class ModelUsuarios(models.Model):
    id = models.AutoField(primary_key=True, unique=True, db_index=True, serialize=True)
    name = models.CharField(max_length=200, blank=False, null=False)
    instituicao = models.CharField(max_length=100, blank=False, null=False)
    funcional = models.IntegerField(blank=False, null=False)
    chefe = models.BooleanField(blank=False, null=False)
    data_registro = models.DateTimeField(auto_now_add=True)
    data_manutencao = models.DateTimeField(auto_now=True)
    id_usuario_django = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'usuarios'
    
class ModelRegistrosAbordagem(models.Model):
    nro_registro = models.AutoField(primary_key=True, unique=True, db_index=True, serialize=True)
    data_registro = models.DateTimeField(auto_now_add=True)
    id_usuario_registro = models.ForeignKey(User, on_delete=models.CASCADE)
    data_manutencao = models.DateTimeField(auto_now=True)
    chefe_guarnicao = models.IntegerField(null=False,blank=False)
    id_tipo_abordagem = models.IntegerField(null=False,blank=False)
    operacao = models.IntegerField(null=True,blank=False)
    
    def __str__(self):
        return f"Registro {self.nro_registro}"

    class Meta:
        db_table = 'registros_abordagem'

class ModelPessoas(models.Model):
    nome = models.CharField(max_length=200, blank=False, null=False)
    data_nascimento = models.DateField(null=False, blank=False)
    nro_documento = models.IntegerField(null=False, blank=False, primary_key=True)
    nome_mae = models.CharField(max_length=200,blank=False, null=False)
    data_registro = models.DateTimeField(auto_now_add=True)
    data_manutencao = models.DateTimeField(auto_now=True)
    id_abordagem = models.ForeignKey(ModelRegistrosAbordagem,on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'pessoas'
        
        
class ModelOperacoes(models.Model):
    nome = models.CharField(max_length=200, blank=False, null=False)
    data_inicio = models.DateTimeField(null=False, blank=False)
    data_fim = models.DateTimeField(null=True)
    municipio = models.CharField(max_length=200,blank=False, null=False)
    bairro = models.CharField(max_length=200,blank=False, null=False)
    comandante = models.CharField(max_length=200,blank=False, null=False)
    data_registro = models.DateTimeField(auto_now_add=True)
    data_manutencao = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'operacoes'

class ModelVeiculos(models.Model):
    tipo_veiculo = models.CharField(max_length=200, blank=False, null=False)
    placa = models.CharField(max_length=200,blank=False, null=False)
    proprietario = models.CharField(max_length=200,blank=False, null=False)
    condutor = models.CharField(max_length=200,blank=False, null=False)
    irregularidade = models.CharField(max_length=200,blank=False, null=True)
    veiculo_apreendido = models.BooleanField(null=True)
    data_registro = models.DateTimeField(auto_now_add=True)
    data_manutencao = models.DateTimeField(auto_now=True)
    id_abordagem = models.ForeignKey(ModelRegistrosAbordagem,on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'veiculos'
        
class ModelEstabelecimentos(models.Model):
    tipo_estabelecimento = models.CharField(max_length=200, blank=False, null=False)
    endereco = models.CharField(max_length=200,blank=False, null=False)
    proprietario = models.CharField(max_length=200,blank=False, null=False)
    irregularidade = models.CharField(max_length=200,blank=False, null=False)
    estabelecimento_interditado = models.BooleanField()
    data_registro = models.DateTimeField(auto_now_add=True)
    data_manutencao = models.DateTimeField(auto_now=True)
    id_abordagem = models.ForeignKey(ModelRegistrosAbordagem,on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'estabelecimento'