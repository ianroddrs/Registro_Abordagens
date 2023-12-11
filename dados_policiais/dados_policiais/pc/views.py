att_joao
import json
from django.core.serializers.json import DjangoJSONEncoder
from time import sleep
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.db import IntegrityError
from django.db.models import Sum,Q
from django.http import HttpResponse, QueryDict
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from mainApp.views import *
from django.contrib.auth.models import User
from mainApp.models import *
from .models import *
import datetime
from .form import *
from mainApp.form import *


@login_required
def nro_ocorrencia(request):
    template = 'nro_ocorrencia.html'
    if request.method == 'GET' and ModelUsuarios.objects.get(id=request.user.id).instituicao == 'PC':
        form_ocorrencia = OcorrenciasForm()
        form_apreensao = ApreensaoForm(prefix='apreensao1')
        form_pessoas = PessoasForm(prefix='pessoa1')
        operacoes, chefes, instituicao = base(request)
        context = {'operacoes':operacoes,
                'chefes': chefes,
                'instituicao': instituicao,
                'form_pessoa': form_pessoas,
                'form_ocorrencia': form_ocorrencia,
                'form_apreensao': form_apreensao,
                }
        return render(request, template,context)
    elif request.POST:
        form_ocorrencia = OcorrenciasForm(request.POST)
        if request.POST.get('nro_bop'):
            try:
                ModelBop.objects.get(nro_bop=request.POST.get('nro_bop'))
                return HttpResponse('Esse numero de ocorrencia ja esta cadastrado')
            except: pass
            bop_apreensao = []
            if form_ocorrencia.is_valid():
                ocorrencia = ModelBop(nro_bop=request.POST.get('nro_bop'),apresentacao='True' if request.POST.get('apresentacao') else 'False',fato_relevante='True' if request.POST.get('fato_relevante') else 'False',enquadramento=request.POST.get('enquadramento'),id_usuario=ModelUsuarios.objects.get(id=request.user.id),id_operacao=ModelOperacoes.objects.get(id=request.POST.get('nome_op')),id_comandante=ModelUsuarios.objects.get(id=request.POST.get('chefe_guarnicao')),cumprimento_medidas='True' if request.POST.get('cumprimento_medidas') else 'False',instituicao=request.POST.get('instituicao') if request.POST.get('instituicao') else None,processo=request.POST.get('processo') if request.POST.get('processo') else None)
                ocorrencia.save()
                try:
                    for prefix in range(1,int(request.POST.get('qtd_apreensao'))+1):
                        apreensao = ApreensaoForm(request.POST,prefix=f'apreensao{prefix}')
                        if apreensao.is_valid():
                            apreensao = apreensao.save()
                            bop_ap = ModelBop_Apreensao(nro_bop=ocorrencia,id_apreensao=apreensao)
                            bop_ap.save()
                            bop_apreensao.append(model_to_dict(apreensao))
                except IntegrityError:
                    pass
                
                pessoas = save_pessoas(request,ModelBop_Pessoa, ocorrencia)
                context = {
                    'registro':model_to_dict(ocorrencia),
                    'registro_pessoas':pessoas,
                    'registro_item':bop_apreensao,
                    'instituicao': ModelUsuarios.objects.get(id=request.user.id).instituicao,
                }
                context_json = json.dumps(context, cls=DjangoJSONEncoder)
                request.session['context'] = context_json
                return redirect('extrato')
            else:
                return HttpResponse('nao salvo')
    else: return render(request, '404.html')

@login_required
def proced_policial(request):
    # try:
        template = 'proced_policial.html'
        if request.method == 'GET' and ModelUsuarios.objects.get(id=request.user.id).instituicao == 'PC':
            form_proc = ProcedimentoForm()
            bop_proc = BopProcForm()
            form_pessoas = PessoasForm(prefix='pessoa1')
            operacoes, chefes, instituicao = base(request)
            context = {'operacoes':operacoes,
                        'chefes': chefes,
                        'instituicao': instituicao,
                        'form_pessoa': form_pessoas,
                        'form_proc': form_proc,
                        'bop_proc': bop_proc,
                        }
            return render(request, template,context)
        elif request.POST:
            form_procedimento = ProcedimentoForm(request.POST)
            form_bopproc = BopProcForm(request.POST)
            try:
                ocorrencia = ModelBop.objects.get(nro_bop=request.POST.get('nro_bop'))
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
            if form_procedimento.is_valid():
                if proced:
                    bop_proc = ModelBop_Procedimento(nro_bop=ocorrencia,nro_procedimento=proced)
                    bop_proc.save()
                else:
                    proced = ModelProcedimento(nro_procedimento=request.POST.get('nro_procedimento'),enquadramento=request.POST.get('enquadramento'),id_usuario=ModelUsuarios.objects.get(id=request.user.id),id_operacao=ModelOperacoes.objects.get(id=request.POST.get('nome_op')),id_comandante=ModelUsuarios.objects.get(id=request.POST.get('chefe_guarnicao')),data_registro=datetime.datetime.now())
                    proced.save()
                    bop_proc = ModelBop_Procedimento(nro_bop=ocorrencia,nro_procedimento=proced)
                    bop_proc.save()    
                pessoas = save_pessoas(request,ModelProc_Pessoa, proced)
                context = {
                        'registro':model_to_dict(ocorrencia),
                        'registro_pessoas':pessoas,
                        'registro_item':model_to_dict(proced),
                        'instituicao': ModelUsuarios.objects.get(id=request.user.id).instituicao,
                    }
                print(model_to_dict(proced))
                context_json = json.dumps(context, cls=DjangoJSONEncoder)
                request.session['context'] = context_json
                return redirect('extrato')
            else:
                return HttpResponse('nao salvo')
        else: return render(request, '404.html')
    
@login_required
def pc_ocorrencias(request):
    usuario = request.user
    instituicao = ModelUsuarios.objects.get(id=usuario.id).instituicao
    parametro_page = request.GET.get('page','1')
    parametro_limit = request.GET.get('limit','15')
    if not(parametro_limit.isdigit() and int(parametro_limit)>0):
        parametro_limit = '15'
    
    Registros = ModelBop.objects.filter(id_usuario=request.user.id).order_by('-data_registro')
    busca = request.GET.get('busca')
    if busca:
        Registros = ModelBop.objects.filter(Q(nro_bop__icontains=busca)|Q(enquadramento__icontains=busca)).order_by('-data_registro')
    else:
        Registros = ModelBop.objects.filter(id_usuario=request.user.id).order_by('-data_registro')
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
    return render(request, 'registro_acoes_pc.html',context)




