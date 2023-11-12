from time import sleep
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
        form_pessoa1 = PessoasForm(prefix='pessoa1')
        form_pessoa2 = PessoasForm(prefix='pessoa2')
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
        
        form_pessoa1 = PessoasForm(request.POST, prefix='pessoa1')
        form_pessoa2 = PessoasForm(request.POST, prefix='pessoa2')
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
        form_pessoa1 = PessoasForm(request.POST, prefix='pessoa1')
        form_pessoa2 = PessoasForm(request.POST, prefix='pessoa2')
        
        #chek pessoas
        pessoa1 = check_pessoas(request,id_pessoa=request.POST.get('pessoa1-id_pessoa'))
        pessoa2 = check_pessoas(request,id_pessoa=request.POST.get('pessoa2-id_pessoa'))
        if request.POST.get('nro_bop'):
            try:
                ModelOcorrencias.objects.get(nro_bop=request.POST.get('nro_bop'))
                return HttpResponse('Esse numero de ocorrencia ja esta cadastrado')
            except: pass
            
            if form_pessoa2.is_valid() and form_pessoa1.is_valid():
                pessoa1 = update_pessoa(form_pessoa=form_pessoa1,pessoa=pessoa1) if pessoa1 else pessoa1
                pessoa2 = update_pessoa(form_pessoa=form_pessoa2,pessoa=pessoa2) if pessoa2 else pessoa2
                relator = pessoa1 if pessoa1 else form_pessoa1.save()
                
                suspeito = pessoa2 if pessoa2 else form_pessoa2.save()
                
                ocorrencia = ModelOcorrencias(nro_bop=request.POST.get('nro_bop'),apresentacao='True' if request.POST.get('apresentacao') else 'False',fato_relevante='True' if request.POST.get('fato_relevante') else 'False',enquadramento=request.POST.get('enquadramento'),id_suspeito=suspeito,id_relator=relator,id_usuario=ModelUsuarios.objects.get(id=request.user.id),id_operacao=ModelOperacoes.objects.get(id=request.POST.get('nome_op')),id_comandante=ModelUsuarios.objects.get(id_usuario_django=request.POST.get('chefe_guarnicao')),cumprimento_medidas='True' if request.POST.get('cumprimento_medidas') else 'False',instituicao=request.POST.get('instituicao') if request.POST.get('instituicao') else None,processo=request.POST.get('processo') if request.POST.get('processo') else None)
                
                ocorrencia.save()
                
                context = {
                    'registro':ocorrencia,
                    'pessoa1':relator,
                    'pessoa2':suspeito,
                    'instituicao': ModelUsuarios.objects.get(id_usuario_django=request.user.id).instituicao,
                }

                return render(request, 'extrato.html', context)
            else:
                return HttpResponse('nao salvo')
        else:
            form_ocorrencia = OcorrenciasForm(request.POST)
        
        form_pessoa1 = PessoasForm(request.POST, prefix='pessoa1')
        form_pessoa2 = PessoasForm(request.POST, prefix='pessoa2')
        context = {
            'chefe_guarnicao': chefes_operacao(request).get('chefe_guarnicao'),
            'chefes': chefes_operacao(request).get('chefes'),
            'nome_op': chefes_operacao(request).get('nome_op'),
            'operacoes': chefes_operacao(request).get('operacoes'),
            'instituicao': ModelUsuarios.objects.get(id_usuario_django=request.user.id).instituicao,
            'form_pessoa2': form_pessoa2,
            'form_pessoa1': form_pessoa1,
            'form_ocorrencia': form_ocorrencia,
            'erro':'O numero da ocorrencia precisa ser preenchido'
        }
    return render(request, template, context)

@login_required
def proced_policial(request):
    try:
        template = 'proced_policial.html'
        if request.method == 'GET':
            operacoes = ModelOperacoes.objects.filter(data_inicio__lte=datetime.datetime.now(),data_fim__gte=datetime.datetime.now())
            chefes = ModelUsuarios.objects.filter(comandante='True')
            usuario = request.user
            instituicao = ModelUsuarios.objects.get(id_usuario_django=usuario.id).instituicao
            form_procedimento = ProcedimentoForm()
            form_bopproc = BopProcForm()
            form_pessoa1 = PessoasForm(prefix='pessoa1')
            form_pessoa2 = PessoasForm(prefix='pessoa2')
            context = {
                'instituicao':instituicao,
                'form_procedimento':form_procedimento,
                'form_pessoa1': form_pessoa1,
                'form_pessoa2': form_pessoa2,
                'operacoes':operacoes,
                'chefes':chefes,
            }
            return render(request, template, context)
        
        elif  'pesquisar' in request.POST.keys() :
            form_procedimento = ProcedimentoForm(request.POST)
            form_bopproc = BopProcForm(request.POST)
            form_pessoa1 = PessoasForm(request.POST, prefix='pessoa1')
            form_pessoa2 = PessoasForm(request.POST, prefix='pessoa2')
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
                'form_bopproc': form_bopproc,
                'form_procedimento': form_procedimento,
            }
        else:
            form_procedimento = ProcedimentoForm(request.POST)
            form_bopproc = BopProcForm(request.POST)
            form_pessoa1 = PessoasForm(request.POST, prefix='pessoa1')
            form_pessoa2 = PessoasForm(request.POST, prefix='pessoa2')
            
            #chek pessoas
            pessoa1 = check_pessoas(request,id_pessoa=request.POST.get('pessoa1-id_pessoa'))
            pessoa2 = check_pessoas(request,id_pessoa=request.POST.get('pessoa2-id_pessoa'))
            
            # except: pass
            try:
                ocorrencia = ModelOcorrencias.objects.get(nro_bop=request.POST.get('nro_bop'))
            except: 
                return HttpResponse('Esse Boletim nao existe no banco de dados. portanto nao pode ser associado a um procedimento')
            try:
                proced = ModelProcedimento.objects.get(nro_procedimento=request.POST.get('nro_procedimento'))
            except: 
                proced = None
            try:
                bop_proc = ModelBop_Procedimento.objects.get(nro_bop=ocorrencia,nro_procedimento=proced)
                return HttpResponse('Esse Boletim ja esta vinculado a esse procedimento')
            except:
                pass
            print(proced)
            if form_pessoa2.is_valid() and form_pessoa1.is_valid() and form_procedimento.is_valid():
                pessoa1 = update_pessoa(form_pessoa=form_pessoa1,pessoa=pessoa1) if pessoa1 else pessoa1
                pessoa2 = update_pessoa(form_pessoa=form_pessoa2,pessoa=pessoa2) if pessoa2 else pessoa2
                if proced:
                    bop_proc = ModelBop_Procedimento(nro_bop=ocorrencia,nro_procedimento=proced)
                    bop_proc.save()
                    context = {
                        'registro':ocorrencia,
                        'proced':proced,
                        'pessoa1':pessoa1,
                        'pessoa2':pessoa2,
                        'instituicao': ModelUsuarios.objects.get(id_usuario_django=request.user.id).instituicao,
                    }
                    return render(request, 'extrato.html', context)
                else:
                    apresentante = pessoa1 if pessoa1 else form_pessoa1.save()
                    autor = pessoa2 if pessoa2 else form_pessoa2.save()

                    Procedimento = ModelProcedimento(nro_procedimento=request.POST.get('nro_procedimento'),apresentacao='True' if request.POST.get('apresentacao') else 'False',fato_relevante='True' if request.POST.get('fato_relevante') else 'False',enquadramento=request.POST.get('enquadramento'),id_autor=autor,id_apresentante=apresentante,id_usuario=ModelUsuarios.objects.get(id=request.user.id),id_operacao=ModelOperacoes.objects.get(id=request.POST.get('nome_op')),id_comandante=ModelUsuarios.objects.get(id_usuario_django=request.POST.get('chefe_guarnicao')),data_registro=datetime.datetime.now())
                    
                    Procedimento.save()
                    print(Procedimento)
                    bop_proc = ModelBop_Procedimento(nro_bop=ocorrencia,nro_procedimento=Procedimento)
                    bop_proc.save()    
                    context = {
                        'registro':ocorrencia,
                        'proced':Procedimento,
                        'pessoa1':apresentante,
                        'pessoa2':autor,
                        'instituicao': ModelUsuarios.objects.get(id_usuario_django=request.user.id).instituicao,
                    }
                    return render(request, 'extrato.html', context)
            return HttpResponse('nao salvo')
    except 	ValueError:
        form_procedimento = ProcedimentoForm(request.POST)
        form_bopproc = BopProcForm(request.POST)
        form_pessoa1 = PessoasForm(request.POST, prefix='pessoa1')
        form_pessoa2 = PessoasForm(request.POST, prefix='pessoa2')
        context = {
                'chefe_guarnicao': chefes_operacao(request).get('chefe_guarnicao'),
                'chefes': chefes_operacao(request).get('chefes'),
                'nome_op': chefes_operacao(request).get('nome_op'),
                'operacoes': chefes_operacao(request).get('operacoes'),
                'instituicao': ModelUsuarios.objects.get(id_usuario_django=request.user.id).instituicao,
                'form_pessoa2': form_pessoa2,
                'form_pessoa1': form_pessoa1,
                'form_bopproc': form_bopproc,
                'form_procedimento': form_procedimento,
            }

    return render(request, template,context)

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
        if pesquisa.isdigit():
            Pessoa = ModelPessoas.objects.filter(Q(nro_documento__icontains=int(pesquisa))).order_by('nome_completo')
            print('oiiiiiiiiiiiiiiii')
        else:
            Pessoa = ModelPessoas.objects.filter(Q(nome_completo__icontains=pesquisa)|Q(nome_mae__icontains=pesquisa)|Q(nome_pai__icontains=pesquisa)).order_by('nome_completo')
            print('22222222222222222')
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

def check_pessoas(request,id_pessoa):
    try: pessoa = ModelPessoas.objects.get(id_pessoa=id_pessoa)
    except: pessoa = None
    return pessoa

def update_pessoa(form_pessoa,pessoa):
    dados_formulario = form_pessoa.cleaned_data
    for campo, valor_formulario in dados_formulario.items():
        valor_pessoa1 = getattr(pessoa, campo)

        # Se houver diferença, atualiza o valor em pessoa1
        if valor_pessoa1 != valor_formulario:
            setattr(pessoa, campo, valor_formulario)

        # Salva as alterações em pessoa1
        pessoa.save()
    return pessoa