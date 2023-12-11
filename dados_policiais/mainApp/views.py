import json
from django.template.loader import render_to_string
from django.forms.models import model_to_dict
from django.http import JsonResponse
import datetime
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.db.models import Sum,Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import *
from mainApp.form import *
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
        instituicao = ModelUsuarios.objects.get(id=usuario.id).instituicao
    except:
        instituicao = 'NAO DEFINIDO'
    try:
        funcional = ModelUsuarios.objects.get(id=usuario.id).funcional
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
    instituicao = ModelUsuarios.objects.get(id=usuario.id).instituicao
    template = 'dashboard.html'
    context = {
        "instituicao":instituicao,
    }
    return render(request, template, context)

@login_required
def indicadores(request):
    template = 'indicadores.html'
    usuario = request.user
    instituicao = ModelUsuarios.objects.get(id=usuario.id).instituicao
    indicadores_page = ModelIndicadores.objects.all()
    context = {
        'indicadores':indicadores_page,
        'instituicao':instituicao,
        }
    return render(request, template, context)

@login_required
def usuario(request):
    usuario = request.user
    instituicao = ModelUsuarios.objects.get(id=usuario.id).instituicao
    template = 'cadastro_usuario.html'
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
        instituicao = ModelUsuarios.objects.get(id=usuario.id).instituicao
        carteira_funcional = form_pessoa1['nro_documento'].value()
        comandante = request.POST.get('chefe_guarnicao')
        
        user = User.objects.filter(username=nome_completo)
        nome = ModelUsuarios.objects.filter(nome_completo=nome_completo)
        pessoa = ModelPessoas.objects.filter(nome_completo=nome_completo)
        
        usuario_cadastrado = True if user and nome else False
        print(usuario_cadastrado)
        user = user if user else User.objects.create_user(username=nome_completo, password=senha)
        nome = nome if nome else ModelUsuarios(nome_completo=nome_completo, instituicao=instituicao, funcional=carteira_funcional, comandante='True' if comandante == 'on' else 'False', id=user).save()
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
    instituicao = ModelUsuarios.objects.get(id=usuario.id).instituicao
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
    return redirect('registro_operacoes')

@login_required
def registro_acoes(request):
    usuario = request.user
    instituicao = ModelUsuarios.objects.get(id=usuario.id).instituicao
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
    return render(request, 'registro_acoes.html',context)

@login_required
def registro_operacoes(request):
    usuario = request.user
    instituicao = ModelUsuarios.objects.get(id=usuario.id).instituicao
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
    return render(request, 'registro_operacoes.html',context)

def registro_acao(request, id):
    template = 'registro_acao.html'
    usuario = request.user
    instituicao = ModelUsuarios.objects.get(id=usuario.id).instituicao
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

def pesquisa_ajax(request):
    if request.GET.get('q'):
        url_parameter = request.GET.get("q")
        list_pessoa = []
        pessoa = ModelPessoas.objects.filter(Q(nome_completo__icontains=url_parameter)|Q(nome_mae__icontains=url_parameter)|Q(nome_pai__icontains=url_parameter)|Q(nro_documento__icontains=url_parameter))
        for p in pessoa:
            list_pessoa.append(model_to_dict(p))
        print(list_pessoa)

        cx = {'resultados_pessoa': list_pessoa}
        template = "includes/resultados_pesquisa.html"

    does_req_accept_json = request.accepts("application/json")
    is_ajax_request = request.headers.get("x-requested-with") == "XMLHttpRequest" and does_req_accept_json

    if is_ajax_request:
        html = render_to_string(
            template_name=template, 
            context=cx
        )

        data_dict = {"html_from_view": html}

        return JsonResponse(data=data_dict, safe=False)
    
def check_pessoas(request,id_pessoa):
    try: pessoa = ModelPessoas.objects.get(id_pessoa=id_pessoa)
    except: pessoa = None
    return pessoa

def update_pessoa(form_pessoa,pessoa):
    dados_formulario = form_pessoa.cleaned_data
    for campo, valor_formulario in dados_formulario.items():
        if campo == 'atuacao':
            continue
        valor_pessoa1 = getattr(pessoa, campo)
        if valor_pessoa1 != valor_formulario:
            setattr(pessoa, campo, valor_formulario)
        pessoa.save()
    return pessoa


@login_required
def extrato(request):
   context_json = request.session.get('context')
   context = json.loads(context_json)
   context.update({
        'instituicao': ModelUsuarios.objects.get(id=request.user.id).instituicao,
        'usuario': request.user
       })
   return render(request, 'extrato.html', context)


def request_pessoa(pesquisa):
    if pesquisa:
        if pesquisa.isdigit():
            Pessoa = ModelPessoas.objects.filter(Q(nro_documento__icontains=int(pesquisa))).order_by('nome_completo')
        else:
            Pessoa = ModelPessoas.objects.filter(Q(nome_completo__icontains=pesquisa)|Q(nome_mae__icontains=pesquisa)|Q(nome_pai__icontains=pesquisa)).order_by('nome_completo')
        return Pessoa

def chefes_operacao(request):
    chefe_guarnicao = request.POST.get('chefe_guarnicao')
    chefe_guarnicao = ModelUsuarios.objects.get(id=chefe_guarnicao)
    chefes = ModelUsuarios.objects.filter(comandante='True').exclude(id=chefe_guarnicao.id)
    nome_op = request.POST.get('nome_op')
    nome_op = ModelOperacoes.objects.get(id=nome_op)
    operacoes = ModelOperacoes.objects.filter(data_inicio__lte=datetime.datetime.now(),data_fim__gte=datetime.datetime.now()).exclude(id=nome_op.id)
    context = {
        'nome_op':nome_op,
        'chefe_guarnicao':chefe_guarnicao,
        'operacoes':operacoes,
    }
    return context

def save_pessoas(request,model, registro):
    pessoas = []
    form_pessoas = []
    registros_pessoas = []
    for prefix in range(1,int(request.POST.get('qtd_pessoas'))+1):
        form_pessoas.append(PessoasForm(request.POST,prefix=f'pessoa{prefix}'))
    for pessoa in form_pessoas:
        pessoa_check = check_pessoas(request,id_pessoa=pessoa['id_pessoa'].value())
        if pessoa.is_valid():
            if pessoa_check:
                pessoa_update = update_pessoa(form_pessoa=pessoa,pessoa=pessoa_check)
                pessoa_save = pessoa_update
            else:
                pessoa_save = pessoa.save()
        if model == 'ModelBop_Pesssoa':
            print('oi')
            atuacao = ModelAtuacao.objects.get(ds_atuacao=pessoa['atuacao'].value())
            print(atuacao)
            bop_pessoa = ModelBop_Pessoa(nro_bop=registro,id_pessoa=pessoa_save,id_atuacao=atuacao)
            bop_pessoa.save()
            registros_pessoas.append(model_to_dict(bop_pessoa))
            
        elif model == 'ModelRegistrosPessoaspcepa':
            registro_pessoa = ModelRegistrosPessoaspcepa(protocolo=registro,id_pessoa=pessoa_save)
            registro_pessoa.save()
            registros_pessoas.append(model_to_dict(registro_pessoa))
            
        elif model == 'ModelBop_Procedimento':
            atuacao = ModelAtuacao.objects.get(ds_atuacao=pessoa['atuacao'].value())
            proced_pessoa = ModelProc_Pessoa(id_atuacao=atuacao, id_pessoa=pessoa_save, nro_procedimento=registro)
            proced_pessoa.save()
            registros_pessoas.append(model_to_dict(proced_pessoa))
        print(registro)
        pessoas.append(model_to_dict(pessoa_save))
    return pessoas

def base(request):
    operacoes = ModelOperacoes.objects.filter(data_inicio__lte=datetime.datetime.now(),data_fim__gte=datetime.datetime.now())
    chefes = ModelUsuarios.objects.filter(comandante='True')
    try:
        instituicao = ModelUsuarios.objects.get(id=request.user.id).instituicao
    except:
        instituicao = 'NAO DEFINIDO'
    return operacoes, chefes, instituicao