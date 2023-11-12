import json
import datetime
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.db.models import Sum,Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from pc.form import *
from pc.views import *
from .models import *
import requests
from PIL import Image
from io import BytesIO
import base64
import re

@login_required
def sair(request):
    template = 'login'
    logout(request)
    return redirect(reverse_lazy(template))

@login_required
def home(request):
    usuario = request.user
    try:
        instituicao = ModelUsuarios.objects.get(id_usuario_django=usuario.id).instituicao
    except:
        instituicao = 'NAO DEFINIDO'
    try:
        funcional = ModelUsuarios.objects.get(id_usuario_django=usuario.id).funcional
    except:
        funcional = 'NAO DEFINIDA'
    gu = 'NAO DEFINIDA'
    template = 'home.html'
    context = {"usuario":usuario,
               "instituicao":instituicao,
               "funcional":funcional,
               "gu":gu,
               }
    return render(request, template, context)

@login_required
def dashboard(request):
    usuario = request.user
    instituicao = ModelUsuarios.objects.get(id_usuario_django=usuario.id).instituicao
    template = 'dashboard.html'
    context = {
        "instituicao":instituicao,
    }
    return render(request, template, context)

@login_required
def acoes(request):
    template = 'acoes.html'
    usuario = request.user
    instituicao = ModelUsuarios.objects.get(id_usuario_django=usuario.id).instituicao
    indicadores_page = ModelIndicadores.objects.all()
    context = {
        'indicadores':indicadores_page,
        'instituicao':instituicao,
        }
    return render(request, template, context)

@login_required
def usuario(request):
    usuario = request.user
    instituicao = ModelUsuarios.objects.get(id_usuario_django=usuario.id).instituicao
    template = 'usuario.html'
    if request.method == 'GET':
        form_pessoa1 = PessoasForm(prefix='pessoa1')
        context = {
            "instituicao":instituicao,
            "form_pessoa1":form_pessoa1,
        }
        return render(request, template, context)
    else:
        form_pessoa1 = PessoasForm(request.POST, prefix='pessoa1')
        
        nome_completo = form_pessoa1['nome_completo'].value()
        senha = request.POST.get('password')
        instituicao = ModelUsuarios.objects.get(id_usuario_django=usuario.id).instituicao
        carteira_funcional = form_pessoa1['nro_documento'].value()
        comandante = request.POST.get('chefe_guarnicao')
        
        user = User.objects.filter(username=nome_completo)
        nome = ModelUsuarios.objects.filter(nome_completo=nome_completo)
        pessoa = ModelPessoas.objects.filter(nome_completo=nome_completo)
        
        usuario_cadastrado = True if user and nome else False
        print(usuario_cadastrado)
        user = user if user else User.objects.create_user(username=nome_completo, password=senha)
        nome = nome if nome else ModelUsuarios(nome_completo=nome_completo, instituicao=instituicao, funcional=carteira_funcional, comandante='True' if comandante == 'on' else 'False', id_usuario_django=user).save()
        if pessoa:
            pessoa = pessoa
        else:
            if form_pessoa1.is_valid():
                form_pessoa1.save()
                context = {
                "instituicao":instituicao,
                "sucess":'Usuario cadastrado com sucesso',
                "form_pessoa1":form_pessoa1,
                }
                return render(request, template, context)
            else:
                context = {
                "instituicao":instituicao,
                "form_pessoa1":form_pessoa1,
                }
                return render(request, template, context)
        if usuario_cadastrado:
            context = {
                "instituicao":instituicao,
                "erro":'Usuario ja cadastrado',
                "form_pessoa1":form_pessoa1,
                }
            return render(request, template, context)
    return render(request, template, context)

@login_required
def cad_operacao(request):
    usuario = request.user
    instituicao = ModelUsuarios.objects.get(id_usuario_django=usuario.id).instituicao
    template = 'cadastro_operacao.html'
    if request.method == "GET":

        context = {
        "instituicao":instituicao,
        }
        return render(request,template, context)
    else:
        nome_operacao = request.POST.get('nome_operacao')
        data_inicio = request.POST.get('data_inicio')
        data_fim = request.POST.get('data_fim')
        comandante = request.POST.get('comandante')
    if ModelOperacoes.objects.filter(nome_operacao=nome_operacao,data_inicio=data_inicio):
        return HttpResponse('Esta operacao já existe')    
    operacao = ModelOperacoes(nome_operacao=nome_operacao,data_inicio=data_inicio,data_fim=data_fim if data_fim else None,responsavel=comandante)
    operacao.save()
    context = {}
    # return HttpResponse('Operacao cadastrada com sucesso')
    return redirect('reg_operacoes')

def get_location_info(latitude, longitude):
    nominatim_url = "https://nominatim.openstreetmap.org/reverse"

    params = {
        "format": "json",
        "lat": latitude,
        "lon": longitude,
    }

    response = requests.get(nominatim_url, params=params)

    if response.status_code == 200:
        data = response.json()
        if "address" in data:
            address = data["address"]
            municipality = address.get("city", address.get("town", address.get("village", "")))
            suburb = address.get("suburb", "")
            state = address.get("state", "")
            return {
                "municipality": municipality,
                "suburb": suburb,
                "state": state,
            }

    return {}

def dms_to_dd(dms):
    degrees, minutes, seconds = dms
    dd = None
    if degrees:
        dd = float(degrees)
    if minutes:
        dd += float(minutes) / 60
    if seconds:
        dd += float(seconds) / 3600
    return dd

@login_required
def cad_abordagem(request):
    template = 'cadastro_abordagem.html'
    if request.method == 'GET':
        # __lte é igual a menor ou igual a, __gte é igual a maior ou igual a
        operacoes = ModelOperacoes.objects.filter(data_inicio__lte=datetime.datetime.now(),data_fim__gte=datetime.datetime.now())
        chefes = ModelUsuarios.objects.filter(comandante='True')
        try:
            instituicao = ModelUsuarios.objects.get(id_usuario_django=request.user.id).instituicao
        except:
            instituicao = 'NAO DEFINIDO'
        context = {'operacoes':operacoes,
                   'chefes': chefes,
                   'instituicao': instituicao,
                   }
        return render(request, template,context)
    else:
        foto_abordado = request.POST.get('foto_abordado')
        foto_documento = request.POST.get('foto_documento')
        nro_documento = request.POST.get('nro_documento')
        nome_envolvido = request.POST.get('nome_envolvido')
        nome_mae = request.POST.get('nome_mae')
        data_nascimento = request.POST.get('data_nasc')
        comandante = request.POST.get('chefe_guarnicao')
        operacao = request.POST.get('nome_op')
        
        imagem_abordado = foto_abordado
        foto_abordado = re.sub('^data:image/.+;base64,', '', foto_abordado)
        image_data = base64.b64decode(foto_abordado)
        img = Image.open(BytesIO(image_data))
        exif_data = img._getexif()
        print(request.POST.get('locationResult'))
        
        if exif_data and 0x8825 in exif_data:
            gps_info = exif_data[0x8825]
            latitude = dms_to_dd(gps_info.get(2, [None]))
            longitude = dms_to_dd(gps_info.get(4, [None]))
            # Assumir a direção como "N" para latitude e "E" para longitude se não especificada
            if "N" not in gps_info.get(3, ["N"]):
                latitude *= -1
            if "W" in gps_info.get(3, []):
                longitude *= -1
            location_info = get_location_info(latitude, longitude)
            print("Latitude (DD):", latitude)
            print("Longitude (DD):", longitude)
            print("Município:", location_info.get("municipality", "N/A"))
            print("Bairro:", location_info.get("suburb", "N/A"))
            print("Estado:", location_info.get("state", "N/A"))
        
        user_ip = get_client_ip(request)
        location_data = get_location_by_ip(user_ip)
        latitude_ip = location_data['latitude']
        longitude_ip = location_data['longitude']
        print(latitude_ip, ',',longitude_ip, '--')
    usuario = ModelUsuarios.objects.get(id=request.user.id)
    
    print(imagem_abordado[:30])
    operacao = ModelOperacoes.objects.get(id=operacao)
    imagem = ModelImagens(imagem=imagem_abordado)
    imagem.save()
    pessoa = ModelPessoas.objects.get(id_pessoa=nome_envolvido)
    abordagem = ModelRegistrosAbordagem(comandante=comandante,id_usuario=usuario,id_operacao=operacao if operacao else None, id_envolvido=pessoa,id_foto_abordado=imagem)
    
    abordagem.save()

    
    context = {}
    # return HttpResponse('Abordagem cadastrada com sucesso')
    return redirect('reg_acoes')

def get_client_ip(request):
    # Tente obter o IP público do cliente usando um serviço externo
    try:
        external_ip = requests.get('https://ipinfo.io').text.strip()
        return external_ip
    except requests.RequestException:
        pass

    # Caso não seja possível obter o IP público, obtenha o IP local
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_location_by_ip(ip):
    url = f"https://ipinfo.io/{ip}/json"
    response = requests.get(url)
    if response.status_code == 200:
        data = json.loads(response.text)
        if 'loc' in data:
            latitude, longitude = data['loc'].split(',')
            return {'latitude': latitude, 'longitude': longitude}
    return {'latitude': 0, 'longitude': 0}

@login_required
def abordagem_veicular(request):
    template = 'cadastro_veiculo.html'
    if request.method == 'GET':
        # __lte é igual a menor ou igual a, __gte é igual a maior ou igual a
        operacoes = ModelOperacoes.objects.filter(data_inicio__lte=datetime.datetime.now(),data_fim__gte=datetime.datetime.now())
        chefes = ModelUsuarios.objects.filter(comandante='True')
        context = {'operacoes':operacoes,
                   'chefes': chefes,
                   }
        return render(request, template,context)
    else:
        tipo_veiculo = request.POST.get('tipo_veiculo')
        placa = request.POST.get('placa')
        nome_proprietario = request.POST.get('proprietario')
        nome_condutor = request.POST.get('condutor')
        irregularidade = request.POST.get('irregularidade')
        veiculo_apreendido = request.POST.get('veiculo_apreendido')
        comandante = request.POST.get('chefe_guarnicao')
        operacao = request.POST.get('nome_op')
    
    usuario = User.objects.get(id=request.user.id)
    
    abordagem = ModelRegistrosAbordagem(comandante=comandante,id_usuario_id=usuario,operacao=operacao if operacao else None,id_tipo_abordagem=2)
    abordagem.save()

    Veiculo = ModelVeiculos(tipo_veiculo=tipo_veiculo,placa=placa,proprietario=nome_proprietario,condutor=nome_condutor,irregularidade=irregularidade,veiculo_apreendido='True' if veiculo_apreendido == 'on' else 'False',id_abordagem=abordagem)
    print(Veiculo)
    Veiculo.save()
    context = {}
    return redirect('acoes')

@login_required
def fiscalizacao_estabelecimento(request):
    template = 'cadastro_estabelecimento.html'
    if request.method == 'GET':
        # __lte é igual a menor ou igual a, __gte é igual a maior ou igual a
        operacoes = ModelOperacoes.objects.filter(data_inicio__lte=datetime.datetime.now(),data_fim__gte=datetime.datetime.now())
        chefes = ModelUsuarios.objects.filter(comandante='True')
        context = {'operacoes':operacoes,
                   'chefes': chefes,
                   }
        return render(request, template,context)
    else:
        tipo_estabelecimento = request.POST.get('tipo_estabelecimento')
        endereco = request.POST.get('endereco')
        proprietario = request.POST.get('proprietario')
        irregularidade = request.POST.get('irregularidade')
        estabelecimento_interditado = request.POST.get('estabelecimento_interditado')
        comandante = request.POST.get('chefe_guarnicao')
        operacao = request.POST.get('nome_op')
        
    usuario = User.objects.get(id=request.user.id)
    
    abordagem = ModelRegistrosAbordagem(comandante=comandante,id_usuario_id=usuario,operacao=operacao if operacao else None,id_tipo_abordagem=3)
    abordagem.save()

    estabelecimento = ModelEstabelecimentos(tipo_estabelecimento=tipo_estabelecimento,endereco=endereco,proprietario=proprietario,irregularidade=irregularidade,estabelecimento_interditado='True' if estabelecimento_interditado == 'on' else 'False',id_abordagem=abordagem)
    print(estabelecimento)
    estabelecimento.save()
    context = {}
    return HttpResponse('fiscalizacao de estabelecimento cadastrada com sucesso')

@login_required
def reg_acoes(request):
    usuario = request.user
    instituicao = ModelUsuarios.objects.get(id_usuario_django=usuario.id).instituicao
    parametro_page = request.GET.get('page','1')
    parametro_limit = request.GET.get('limit','15')
    if not(parametro_limit.isdigit() and int(parametro_limit)>0):
        parametro_limit = '15'
    
    Registros = ModelRegistrosAbordagem.objects.filter(id_usuario=request.user.id).order_by('-data_registro')
    busca = request.GET.get('busca')
    if busca:
        Registros = ModelRegistrosAbordagem.objects.filter(Q(nro_registro__icontains=busca)|Q(tipo_servico__icontains=busca)).order_by('-data_registro')
    else:
        Registros = ModelRegistrosAbordagem.objects.filter(id_usuario=request.user.id).order_by('-data_registro')
    ocorrencias_paginator = Paginator(Registros,parametro_limit)
    try:
        page = ocorrencias_paginator.page(parametro_page)
    except (EmptyPage, PageNotAnInteger):
        page = ocorrencias_paginator.page(1)
    operacoes = ModelOperacoes.objects.all()
    chefes = ModelUsuarios.objects.all()
    context = {
        'quantidade_por_pagina': ['10','15','25','50','100'],
        'limitp': parametro_limit,
        "instituicao":instituicao,
        'registro': page,
        'operacao': operacoes,
        'chefes':chefes
    }
    return render(request, 'reg_acoes.html',context)

@login_required
def reg_operacoes(request):
    usuario = request.user
    instituicao = ModelUsuarios.objects.get(id_usuario_django=usuario.id).instituicao
    parametro_page = request.GET.get('page','1')
    parametro_limit = request.GET.get('limit','50')
    if not(parametro_limit.isdigit() and int(parametro_limit)>0):
        parametro_limit = '50'
    
    Operacoes = ModelOperacoes.objects.all().order_by('-data_registro')
    busca = request.GET.get('busca')
    if busca:
        Operacoes = ModelOperacoes.objects.filter(Q(nro_registro__icontains=busca)|Q(tipo_servico__icontains=busca)).order_by('-data_registro')
    else:
        Operacoes = ModelOperacoes.objects.all().order_by('-data_registro')
    ocorrencias_paginator = Paginator(Operacoes,parametro_limit)
    try:
        page = ocorrencias_paginator.page(parametro_page)
    except (EmptyPage, PageNotAnInteger):
        page = ocorrencias_paginator.page(1)
    context = {
        'quantidade_por_pagina': ['10','15','25','50','100'],
        "instituicao":instituicao,  
        'limitp': parametro_limit,
        'operacoes': page
    }
    return render(request, 'reg_operacoes.html',context)

def reg_acao(request, id):
    template = 'reg_acao.html'
    usuario = request.user
    instituicao = ModelUsuarios.objects.get(id_usuario_django=usuario.id).instituicao
    if request.method == 'GET':
        registro = ModelRegistrosAbordagem.objects.filter(nro_registro=id).values()
        id_tipo_abordagem = ModelRegistrosAbordagem.objects.get(nro_registro=id).id_tipo_abordagem
        print(id_tipo_abordagem)
        try:
            operacao = ModelOperacoes.objects.get(id=ModelRegistrosAbordagem.objects.get(nro_registro=id).operacao).nome
        except:
            operacao = None
        
        if id_tipo_abordagem.id_tipo_abordagem == 1:
            abordagem = ModelPessoas.objects.filter(nro_registro=id).values()

        elif id_tipo_abordagem.id_tipo_abordagem == 2:
            abordagem = ModelVeiculos.objects.filter(nro_registro=id).values()
            
        elif id_tipo_abordagem.id_tipo_abordagem == 3:
            abordagem = ModelEstabelecimentos.objects.filter(nro_registro=id).values()
        context = {
            'registro':registro,
            'operacao':operacao,
            "instituicao":instituicao,  
            'abordagem':abordagem
        }
        return render(request, template, context)
    else:
        print(request.POST.get('id_tipo_abordagem'))
        if request.POST.get('id_tipo_abordagem') == '1':
            foto_abordado = request.POST.get('foto_abordado')
            foto_documento = request.POST.get('foto_documento')
            nro_documento = request.POST.get('nro_documento')
            nome_envolvido = request.POST.get('nome')
            nome_mae = request.POST.get('nome_mae')
            data_nascimento = request.POST.get('data_nascimento')
            comandante = request.POST.get('chefe_guarnicao')
            operacao = request.POST.get('nome_op')
            # data_registro = request.POST.get('data_registro')
            print(nome_envolvido)
            usuario = User.objects.get(id=request.user.id)
            abordagem = ModelRegistrosAbordagem(nro_registro=id,comandante=comandante,id_usuario_id=usuario,operacao=operacao if operacao else None,id_tipo_abordagem=1,data_registro=datetime.datetime.now())
            abordagem.save()
            
            update_abordagem = ModelPessoas(nome=nome_envolvido,data_nascimento=datetime.datetime.now(),nro_documento=nro_documento,nome_mae=nome_mae,id_abordagem=abordagem, data_registro=datetime.datetime.now())
            
            update_abordagem.save()
            return HttpResponse('salvo')
        return HttpResponse('nao salvo')
    