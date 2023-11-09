from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.db.models import Sum,Q
from django.http import HttpResponse, QueryDict
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from mainApp.models import *
from .models import *
import datetime
from .form import *



@login_required
def nro_ocorrencia(request):
    template = 'nro_ocorrencia.html'
    if request.method == 'GET':
        operacoes = ModelOperacoes.objects.filter(data_inicio__lte=datetime.datetime.now(),data_fim__gte=datetime.datetime.now())
        chefes = ModelUsuarios.objects.filter(comandante='True')
        form_ocorrencia = OcorrenciasForm()
        form_apreensao = ApreensaoForm()
        form_pessoa2 = PessoasForm(prefix='pessoa1')
        form_pessoa1 = PessoasForm(prefix='pessoa2')
        try:
            instituicao = ModelUsuarios.objects.get(id_usuario_django=request.user.id).instituicao
        except:
            instituicao = 'NAO DEFINIDO'
        context = {'operacoes':operacoes,
                   'chefes': chefes,
                   'instituicao': instituicao,
                   'form_pessoa2': form_pessoa2,
                   'form_pessoa1': form_pessoa1,
                   'form_ocorrencia': form_ocorrencia,
                   'form_apreensao': form_apreensao,
                   }
        return render(request, template,context)
    
    elif  'pesquisar' in request.POST.keys() :
        form_ocorrencia = OcorrenciasForm(request.POST)
        
        form_pessoa2 = PessoasForm(request.POST, prefix='pessoa1')
        form_pessoa1 = PessoasForm(request.POST, prefix='pessoa2')
        print(form_ocorrencia)
        context = {
            'pesquisar': request.POST.get('pesquisar'),
            'pesquisa': request.POST.get('input_pesquisa'),
            'chefe_guarnicao': chefes_operacao(request).get('chefe_guarnicao'),
            'chefes': chefes_operacao(request).get('chefes'),
            'nome_op': chefes_operacao(request).get('nome_op'),
            'operacoes': chefes_operacao(request).get('operacoes'),
            'resultados_pesquisa': request_pessoa(request.POST.get('input_pesquisa')),
            'instituicao': ModelUsuarios.objects.get(id_usuario_django=request.user.id).instituicao,
            'form_pessoa2': form_pessoa2,
            'form_pessoa1': form_pessoa1,
            'form_ocorrencia': form_ocorrencia,
        }
    else:
        form_ocorrencia = OcorrenciasForm(request.POST)
        form_pessoa2 = PessoasForm(request.POST, prefix='pessoa1')
        form_pessoa1 = PessoasForm(request.POST, prefix='pessoa2')
        
        #chek pessoas
        pessoa1 = ModelPessoas.objects.get(id_pessoa=request.POST.get('id_pessoa1'))
        pessoa2 = ModelPessoas.objects.get(id_pessoa=request.POST.get('id_pessoa2'))
        
        if form_pessoa2.is_valid() and form_pessoa1.is_valid():
            suspeito = pessoa1 if pessoa1 else form_pessoa2.save()
            relator = pessoa2 if pessoa2 else form_pessoa1.save()
            ocorrencia = ModelOcorrencias(nro_bop=request.POST.get('numero'),apresentacao='True' if request.POST.get('apresentacao') else 'False',fato_relevante='True' if request.POST.get('fato_relevante') else 'False',enquadramento=request.POST.get('enquadramento'),id_suspeito=suspeito,id_relator=relator,id_usuario=ModelUsuarios.objects.get(id=request.user.id),id_operacao=ModelOperacoes.objects.get(id=request.POST.get('nome_op')))
            ocorrencia = ocorrencia.save()

            return HttpResponse('salvo')
        else:
            return HttpResponse('nao salvo')
        
        
    # elif 'pesquisar' in request.POST.keys() :
    #     chefes_operacao(request).get('nome_op')
    #     instituicao = ModelUsuarios.objects.get(id_usuario_django=request.user.id).instituicao
    #     context = {
    #         'pesquisa': request.POST.get('input_pesquisa'),
    #         'chefe_guarnicao': chefes_operacao(request).get('chefe_guarnicao'),
    #         'chefes': chefes_operacao(request).get('chefes'),
    #         'nome_op': chefes_operacao(request).get('nome_op'),
    #         'operacoes': chefes_operacao(request).get('operacoes'),
    #         'resultados_pesquisa': request_pessoa(request.POST.get('input_pesquisa')),
    #         'instituicao': instituicao,
    #     }
        
        # return render(request, template,context)
        
        # apresentacao = request.POST.get('apresentacao')
        # relevante = request.POST.get('fato_relevante')
        # numero = request.POST.get('numero')
        # enquadramento = request.POST.get('enquadramento')
        # relator = request.POST.get('nome_relator')
        # suspeito = request.POST.get('nome_suspeito')
        # genero = request.POST.get('genero')

        # usuario = ModelUsuarios.objects.get(id=request.user.id)
        # operacao = ModelOperacoes.objects.get(id=operacao)
        # relator = ModelPessoas.objects.get(id_pessoa=relator)
        # suspeito = ModelPessoas.objects.get(id_pessoa=suspeito)
        
        # ocorrencia = ModelOcorrencias(nro_bop=numero,apresentacao=apresentacao,fato_relevante=relevante,enquadramento=enquadramento,id_relator=relator,id_suspeito=suspeito,id_usuario=usuario,id_operacao=operacao)
        
        # ocorrencia.save()
    
    return render(request, template, context)

@login_required
def proced_policial(request):
    template = 'proced_policial.html'
    if request.method == 'GET':
        operacoes = ModelOperacoes.objects.filter(data_inicio__lte=datetime.datetime.now(),data_fim__gte=datetime.datetime.now())
        chefes = ModelUsuarios.objects.filter(comandante='True')
        usuario = request.user
        instituicao = ModelUsuarios.objects.get(id_usuario_django=usuario.id).instituicao
        form_procedimento = ProcedimentoForm()
        form_apresentante = PessoasForm(prefix='pessoa1')
        form_autor = PessoasForm(prefix='pessoa2')
        context = {
            'instituicao':instituicao,
            'form_procedimento':form_procedimento,
            'form_apresentante':form_apresentante,
            'form_autor':form_autor,
            'operacoes':operacoes,
            'chefes':chefes,
        }
        return render(request, template, context)
    
    elif 'pesquisar' in request.POST.keys() :
        form_procedimento = ProcedimentoForm(request.POST)
        form_apresentante = PessoasForm(request.POST, prefix='pessoa1')
        form_autor = PessoasForm(request.POST, prefix='pessoa2')
        context = {
            'pesquisar': request.POST.get('pesquisar'),
            'pesquisa': request.POST.get('input_pesquisa'),
            'chefe_guarnicao': chefes_operacao(request).get('chefe_guarnicao'),
            'chefes': chefes_operacao(request).get('chefes'),
            'nome_op': chefes_operacao(request).get('nome_op'),
            'operacoes': chefes_operacao(request).get('operacoes'),
            'resultados_pesquisa': request_pessoa(request.POST.get('input_pesquisa')),
            'instituicao': ModelUsuarios.objects.get(id_usuario_django=request.user.id).instituicao,
            'form_autor': form_autor,
            'form_apresentante': form_apresentante,
            'form_procedimento': form_procedimento,
        }
    else:
        form_procedimento = ProcedimentoForm(request.POST)
        form_apresentante = PessoasForm(request.POST, prefix='pessoa1')
        ocorrencia = ModelOcorrencias.objects.get(nro_bop=request.POST.get('nro_bop'))
        form_autor = PessoasForm(request.POST, prefix='pessoa2')
        
        #REMOVER IF
        if request.POST.get('id_pessoa1') and request.POST.get('id_pessoa2'):
            pessoa1 = ModelPessoas.objects.get(id_pessoa=request.POST.get('id_pessoa1'))
            pessoa2 = ModelPessoas.objects.get(id_pessoa=request.POST.get('id_pessoa2'))
        else:
            pessoa1 = None
            pessoa2 = None
            
        if form_autor.is_valid() and form_apresentante.is_valid():
            apresentante = pessoa1 if pessoa1 else form_apresentante.save()
            autor = pessoa2 if pessoa2 else form_autor.save()
            
            procedimento = ModelProcedimento(nro_bop=ocorrencia,apresentacao='True' if request.POST.get('apresentacao') else 'False',fato_relevante='True' if request.POST.get('fato_relevante') else 'False',enquadramento=request.POST.get('enquadramento'),id_autor=autor,id_apresentante=apresentante,id_usuario=ModelUsuarios.objects.get(id=request.user.id),id_operacao=ModelOperacoes.objects.get(id=request.POST.get('nome_op')))
            
            procedimento = procedimento.save()

            return HttpResponse('salvo')
        else:
            return HttpResponse('nao salvo')
        
    return render(request, template)

@login_required
def apreensao(request):
    template = 'apreensao.html'
    if request.method == 'GET':
        usuario = request.user
        instituicao = ModelUsuarios.objects.get(id_usuario_django=usuario.id).instituicao
        context = {
            'instituicao':instituicao,
        }
        return render(request, template, context)
    return render(request, template)

@login_required
def cumprimento_medidas_cautelares(request):
    template = 'cumprimento_medidas_cautelares.html'
    if request.method == 'GET':
        usuario = request.user
        instituicao = ModelUsuarios.objects.get(id_usuario_django=usuario.id).instituicao
        context = {
            'instituicao':instituicao,
        }
        return render(request, template, context)
    return render(request, template)

@login_required
def pc_ocorrencias(request):
    usuario = request.user
    instituicao = ModelUsuarios.objects.get(id_usuario_django=usuario.id).instituicao
    parametro_page = request.GET.get('page','1')
    parametro_limit = request.GET.get('limit','15')
    if not(parametro_limit.isdigit() and int(parametro_limit)>0):
        parametro_limit = '15'
    
    Registros = ModelOcorrencias.objects.filter(id_usuario=request.user.id).order_by('-data_registro')
    busca = request.GET.get('busca')
    if busca:
        Registros = ModelOcorrencias.objects.filter(Q(nro_bop__icontains=busca)|Q(enquadramento__icontains=busca)).order_by('-data_registro')
    else:
        Registros = ModelOcorrencias.objects.filter(id_usuario=request.user.id).order_by('-data_registro')
    ocorrencias_paginator = Paginator(Registros,parametro_limit)
    try:
        page = ocorrencias_paginator.page(parametro_page)
    except (EmptyPage, PageNotAnInteger):
        page = ocorrencias_paginator.page(1)
    operacoes = ModelOperacoes.objects.all()
    pessoa = ModelPessoas.objects.all()
    chefes = ModelUsuarios.objects.filter(comandante='True')
    context = {
        'quantidade_por_pagina': ['10','15','25','50','100'],
        'limitp': parametro_limit,
        "instituicao":instituicao,
        'registro': page,
        'operacao': operacoes,
        'chefes':chefes,
        'pessoa':pessoa,
    }
    return render(request, 'reg_acoes_pc.html',context)

def request_pessoa(pesquisa):
    if pesquisa:
        Pessoa = ModelPessoas.objects.filter(Q(nome_completo__icontains=pesquisa)|Q(nome_mae__icontains=pesquisa)|Q(nome_pai__icontains=pesquisa)).order_by('nome_completo')
        return Pessoa

def chefes_operacao(request):
    chefe_guarnicao = request.POST.get('chefe_guarnicao')
    chefe_guarnicao = ModelUsuarios.objects.get(id_usuario_django=chefe_guarnicao)
    chefes = ModelUsuarios.objects.filter(comandante='True').exclude(id_usuario_django=chefe_guarnicao.id_usuario_django)
    nome_op = request.POST.get('nome_op')
    nome_op = ModelOperacoes.objects.get(id=nome_op)
    operacoes = ModelOperacoes.objects.filter(data_inicio__lte=datetime.datetime.now(),data_fim__gte=datetime.datetime.now()).exclude(id=nome_op.id)
    context = {
        'nome_op':nome_op,
        'chefe_guarnicao':chefe_guarnicao,
        'operacoes':operacoes,
    }
    return context

def save_relator(request):
    relator = ModelPessoas(nome_completo=request.POST.get('nome_relator') if request.POST.get('nome_relator') else None,
                          data_nascimento=request.POST.get('data_nascimento_relator') if request.POST.get('data_nascimento_relator') else None,
                          genero=request.POST.get('genero_relator') if request.POST.get('genero_relator') else None,
                          nro_documento=request.POST.get('nro_documento_relator') if request.POST.get('nro_documento_relator') else None,
                          nome_mae = request.POST.get('nome_mae_relator') if request.POST.get('nome_mae_relator') else None,
                          nome_pai=request.POST.get('nome_pai_relator') if request.POST.get('nome_pai_relator') else None,
                          endereco_residencial=request.POST.get('endereco_residencial_relator') if request.POST.get('endereco_residencial_relator') else None)
    return relator