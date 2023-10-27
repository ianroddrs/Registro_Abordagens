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

@login_required
def sair(request):
    template = 'login'
    logout(request)
    return redirect(reverse_lazy(template))

@login_required
def home(request):
    usuario = request.user
    try:
        orgao = ModelUsuarios.objects.get(id_usuario_django=usuario.id).instituicao
    except:
        orgao = 'NAO DEFINIDO'
    try:
        funcional = ModelUsuarios.objects.get(id_usuario_django=usuario.id).funcional
    except:
        funcional = 'NAO DEFINIDA'
    gu = 'NAO DEFINIDA'
    template = 'home.html'
    context = {"usuario":usuario,
               "orgao":orgao,
               "funcional":funcional,
               "gu":gu,
               }
    return render(request, template, context)

@login_required
def dashboard(request):
    template = 'dashboard.html'
    context = {}
    return render(request, template, context)

@login_required
def acoes(request):
    template = 'acoes.html'
    context = {}
    return render(request, template, context)

@login_required
def usuario(request):
    template = 'usuario.html'
    if request.method == 'GET':
        return render(request, template)
    
    else:
        username_template = request.POST.get('username')
        print(username_template)
        senha = request.POST.get('password')
        orgao = request.POST.get('instituicao')
        carteira_funcional = request.POST.get('carteira_funcional')
        guarnicao = request.POST.get('guarnicao')
        chefe_guarnicao = request.POST.get('chefe_guarnicao')
        
        user = User.objects.filter(username=username_template)
        nome = ModelUsuarios.objects.filter(name=username_template)
        
        if user:
            return HttpResponse('Já existe esse usuário')
        
        user = User.objects.create_user(username=username_template, password=senha)
        usuario = ModelUsuarios(name=username_template, instituicao=orgao, funcional=carteira_funcional, chefe='True' if chefe_guarnicao == 'on' else 'False', id_usuario_django=user)
        print(user,usuario)
        usuario.save()
            
    return HttpResponse('Usuário criado com sucesso')
    return redirect('home')

@login_required
def cad_operacao(request):
    template = 'cadastro_operacao.html'
    if request.method == "GET":
        return render( request,template)
    else:
        nome_operacao = request.POST.get('nome_operacao')
        data_inicio = request.POST.get('data_inicio')
        data_fim = request.POST.get('data_fim')
        municipio = request.POST.get('municipio')
        bairro = request.POST.get('bairro')
        comandante = request.POST.get('comandante')
    if ModelOperacoes.objects.filter(nome=nome_operacao,data_inicio=data_inicio):
        return HttpResponse('Esta operacao já existe')    
    operacao = ModelOperacoes(nome=nome_operacao,data_inicio=data_inicio,data_fim=data_fim if data_fim else None,municipio=municipio,bairro=bairro,comandante=comandante)
    operacao.save()
    context = {}
    # return HttpResponse('Operacao cadastrada com sucesso')
    return redirect('operacoes')

@login_required
def cad_abordagem(request):
    template = 'cadastro_abordagem.html'
    if request.method == 'GET':
        # __lte é igual a menor ou igual a, __gte é igual a maior ou igual a
        operacoes = ModelOperacoes.objects.filter(data_inicio__lte=datetime.datetime.now(),data_fim__gte=datetime.datetime.now())
        chefes = ModelUsuarios.objects.filter(chefe='True')
        context = {'operacoes':operacoes,
                   'chefes': chefes,
                   }
        return render(request, template,context)
    else:
        foto_abordado = request.POST.get('foto_abordado')
        foto_documento = request.POST.get('foto_documento')
        nro_documento = request.POST.get('nro_documento')
        nome_envolvido = request.POST.get('nome_envolvido')
        nome_mae = request.POST.get('nome_mae')
        data_nascimento = request.POST.get('data_nasc')
        chefe_guarnicao = request.POST.get('chefe_guarnicao')
        operacao = request.POST.get('nome_op')
        base64_image = request.POST.get('base64_image')
        print(base64_image)
        
        print(foto_abordado)
        
    
    usuario = User.objects.get(id=request.user.id)
    
    abordagem = ModelRegistrosAbordagem(chefe_guarnicao=chefe_guarnicao,id_usuario_registro=usuario,id_tipo_abordagem=1,operacao=operacao if operacao else None)
    abordagem.save()

    Pessoa = ModelPessoas(nome=nome_envolvido,data_nascimento=data_nascimento,nro_documento=nro_documento,nome_mae=nome_mae,id_abordagem=abordagem)
    print(Pessoa)
    Pessoa.save()
    context = {}
    # return HttpResponse('Abordagem cadastrada com sucesso')
    return redirect('registros')


@login_required
def abordagem_veicular(request):
    template = 'cadastro_veiculo.html'
    if request.method == 'GET':
        # __lte é igual a menor ou igual a, __gte é igual a maior ou igual a
        operacoes = ModelOperacoes.objects.filter(data_inicio__lte=datetime.datetime.now(),data_fim__gte=datetime.datetime.now())
        chefes = ModelUsuarios.objects.filter(chefe='True')
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
        chefe_guarnicao = request.POST.get('chefe_guarnicao')
        operacao = request.POST.get('nome_op')
    
    usuario = User.objects.get(id=request.user.id)
    
    abordagem = ModelRegistrosAbordagem(chefe_guarnicao=chefe_guarnicao,id_usuario_registro=usuario,operacao=operacao if operacao else None,id_tipo_abordagem=2)
    abordagem.save()

    Veiculo = ModelVeiculos(tipo_veiculo=tipo_veiculo,placa=placa,proprietario=nome_proprietario,condutor=nome_condutor,irregularidade=irregularidade,veiculo_apreendido='True' if veiculo_apreendido == 'on' else 'False',id_abordagem=abordagem)
    print(Veiculo)
    Veiculo.save()
    context = {}
    return redirect('registros')

@login_required
def fiscalizacao_estabelecimento(request):
    template = 'cadastro_estabelecimento.html'
    if request.method == 'GET':
        # __lte é igual a menor ou igual a, __gte é igual a maior ou igual a
        operacoes = ModelOperacoes.objects.filter(data_inicio__lte=datetime.datetime.now(),data_fim__gte=datetime.datetime.now())
        chefes = ModelUsuarios.objects.filter(chefe='True')
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
        chefe_guarnicao = request.POST.get('chefe_guarnicao')
        operacao = request.POST.get('nome_op')
        
    usuario = User.objects.get(id=request.user.id)
    
    abordagem = ModelRegistrosAbordagem(chefe_guarnicao=chefe_guarnicao,id_usuario_registro=usuario,operacao=operacao if operacao else None,id_tipo_abordagem=3)
    abordagem.save()

    estabelecimento = ModelEstabelecimentos(tipo_estabelecimento=tipo_estabelecimento,endereco=endereco,proprietario=proprietario,irregularidade=irregularidade,estabelecimento_interditado='True' if estabelecimento_interditado == 'on' else 'False',id_abordagem=abordagem)
    print(estabelecimento)
    estabelecimento.save()
    context = {}
    return HttpResponse('fiscalizacao de estabelecimento cadastrada com sucesso')

@login_required
def busca_apreensao(request):
    template = 'cadastro_busca_apreensao.html'
    context= {}
    return render(request, template, context)


@login_required
def registros(request):
    parametro_page = request.GET.get('page','1')
    parametro_limit = request.GET.get('limit','15')
    if not(parametro_limit.isdigit() and int(parametro_limit)>0):
        parametro_limit = '15'
    
    Registros = ModelRegistrosAbordagem.objects.filter(id_usuario_registro=request.user.id).order_by('-data_registro')
    busca = request.GET.get('busca')
    if busca:
        Registros = ModelRegistrosAbordagem.objects.filter(Q(nro_registro__icontains=busca)|Q(tipo_servico__icontains=busca)).order_by('-data_registro')
    else:
        Registros = ModelRegistrosAbordagem.objects.filter(id_usuario_registro=request.user.id).order_by('-data_registro')
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
        'registro': page,
        'operacao': operacoes,
        'chefes':chefes
    }
    return render(request, 'registros.html',context)

@login_required
def operacoes(request):
    parametro_page = request.GET.get('page','1')
    parametro_limit = request.GET.get('limit','15')
    if not(parametro_limit.isdigit() and int(parametro_limit)>0):
        parametro_limit = '15'
    
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
        'limitp': parametro_limit,
        'operacoes': page
    }
    return render(request, 'operacoes.html',context)

def view_registro(request, id):
    template = 'registro.html'
    registro = ModelRegistrosAbordagem.objects.filter(nro_registro=id)
    context = {
        'registro':registro
    }
    return render(request, template, context)
    