import json
from django.core.serializers.json import DjangoJSONEncoder
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.db.models import Sum,Q
from django.http import HttpResponse, QueryDict
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from mainApp.models import *
from mainApp.views import *
from .models import *
import datetime
from .form import *
from pc.form import *
from django.template.loader import render_to_string
from pc.views import *
from mainApp.models import *
from mainApp.form import *
from django.forms.models import model_to_dict
from django.urls import reverse


@login_required
def analise_droga(request):
    template = 'analise.html'
    if request.method == 'GET':
        operacoes = ModelOperacoes.objects.filter(data_inicio__lte=datetime.datetime.now(),data_fim__gte=datetime.datetime.now())
        chefes = ModelUsuarios.objects.filter(comandante='True')
        form_registros = RegistrosPCEPAForm()
        form_analise = AnaliseDrogaForm(prefix='analise1')
        form_pessoas = PessoasForm(prefix='pessoa1')
        form_imagem = ImagemForm(prefix='imagem1')
        try:
            instituicao = ModelUsuarios.objects.get(id=request.user.id).instituicao
        except:
            instituicao = 'NAO DEFINIDO'
        context = {'operacoes':operacoes,
                   'chefes': chefes,
                   'instituicao': instituicao,
                   'form_pessoa': form_pessoas,
                   'form_registros': form_registros,
                   'form_analise': form_analise,
                   'form_imagem': form_imagem,
                   }
        return render(request, template,context)
    elif request.POST:
        form_registros = RegistrosPCEPAForm(request.POST)
        if request.POST.get('protocolo'):
            # try:
            #     ModelRegistrospcepa.objects.get(protocolo=request.POST.get('protocolo'))
            #     return HttpResponse('Esse numero de prtocolo ja esta cadastrado')
            # except: pass
            
            analises = []
            imagens = [] 
            if form_registros.is_valid():
                registro = ModelRegistrospcepa(protocolo=request.POST.get('protocolo'),caso=request.POST.get('caso'),bop_tombo=request.POST.get('bop_tombo'),tipo_exame=request.POST.get('tipo_exame'),data_exame=request.POST.get('data_exame'),id_usuario=ModelUsuarios.objects.get(id=request.user.id),id_operacao=ModelOperacoes.objects.get(id=request.POST.get('nome_op')),id_comandante=ModelUsuarios.objects.get(id=request.POST.get('chefe_guarnicao')))
                registro.save()
                for prefix in range(1,2):
                    if request.POST.get(f'imagem{prefix}-imagem'):
                        imagem = ModelImagens(imagem=request.POST.get(f'imagem{prefix}-imagem'))
                        imagem.save()
                        registro_imagem = ModelRegistrosImagens(protocolo=registro,id_imagem=imagem)
                        registro_imagem.save()
                        imagens.append(model_to_dict(imagem))
                # for prefix in range(1,len(request.POST.get('qtd_pessoas'))+1):
                for prefix in range(1,2):
                    analise = AnaliseDrogaForm(request.POST,prefix=f'analise{prefix}')
                    if analise.is_valid():
                        analise = ModelAnaliseDrogapcepa(protocolo=registro, tipo_droga=analise['tipo_droga'].value(),apresentacao=True if analise['apresentacao'].value() else None,qtd=analise['qtd'].value(),und_medida=analise['und_medida'].value())
                        analise.save()
                        analises.append(model_to_dict(analise))
                        print(analise, ' ANALISE')
                pessoas = save_pessoas(request, ModelRegistrosPessoaspcepa, registro)
                context = {
                    'registro':model_to_dict(registro),
                    'registro_pessoas':pessoas,
                    'registro_item':analises,
                    'registro_imagens':imagens,
                }
                context_json = json.dumps(context, cls=DjangoJSONEncoder)
                request.session['context'] = context_json
                return redirect('extrato')
            else:
                return HttpResponse('nao salvo')

@login_required
def analise_balistica(request):
    template = 'analise.html'
    if request.method == 'GET':
        operacoes = ModelOperacoes.objects.filter(data_inicio__lte=datetime.datetime.now(),data_fim__gte=datetime.datetime.now())
        chefes = ModelUsuarios.objects.filter(comandante='True')
        form_registros = RegistrosPCEPAForm()
        form_analise = AnaliseBalisticaForm(prefix='analise1')
        form_pessoas = PessoasForm(prefix='pessoa1')
        form_imagem = ImagemForm(prefix='imagem1')
        try:
            instituicao = ModelUsuarios.objects.get(id=request.user.id).instituicao
        except:
            instituicao = 'NAO DEFINIDO'
        context = {'operacoes':operacoes,
                   'chefes': chefes,
                   'instituicao': instituicao,
                   'form_pessoa': form_pessoas,
                   'form_registros': form_registros,
                   'form_analise': form_analise,
                   'form_imagem': form_imagem,
                   }
        return render(request, template,context)
    elif request.POST:
        form_registros = RegistrosPCEPAForm(request.POST)
        if request.POST.get('protocolo'):
            try:
                ModelRegistrospcepa.objects.get(protocolo=request.POST.get('protocolo'))
                return HttpResponse('Esse numero de prtocolo ja esta cadastrado')
            except: pass
            
            analises = []
            imagens = [] 
            if form_registros.is_valid():
                registro = ModelRegistrospcepa(protocolo=request.POST.get('protocolo'),caso=request.POST.get('caso'),bop_tombo=request.POST.get('bop_tombo'),tipo_exame=request.POST.get('tipo_exame'),data_exame=request.POST.get('data_exame'),id_usuario=ModelUsuarios.objects.get(id=request.user.id),id_operacao=ModelOperacoes.objects.get(id=request.POST.get('nome_op')),id_comandante=ModelUsuarios.objects.get(id=request.POST.get('chefe_guarnicao')))
                registro.save()
                for prefix in range(1,2):
                    if request.POST.get(f'imagem{prefix}-imagem'):
                        imagem = ModelImagens(imagem=request.POST.get(f'imagem{prefix}-imagem'))
                        imagem.save()
                        registro_imagem = ModelRegistrosImagens(protocolo=registro,id_imagem=imagem)
                        registro_imagem.save()
                        imagens.append(model_to_dict(imagem))
                
                # for prefix in range(1,len(request.POST.get('qtd_pessoas'))+1):
                for prefix in range(1,2):
                    
                    analise = AnaliseBalisticaForm(request.POST,prefix=f'analise{prefix}')
                    if analise.is_valid():
                        print(analise['tipo_material'].value())
                        analise = ModelAnaliseBalisticapcepa(protocolo=registro, tipo_material=analise['tipo_material'].value(), calibre=analise['calibre'].value(), nro_serie_rastreio=analise['nro_serie_rastreio'].value(), nro_patrimonio=analise['nro_patrimonio'].value(),qtd=analise['qtd'].value())
                        analise.save()
                        analises.append(model_to_dict(analise))
                        
                form_pessoas = []
                # for prefix in range(1,len(request.POST.get('qtd_pessoas'))+2):
                for prefix in range(1,2):
                    form_pessoas.append(PessoasForm(request.POST,prefix=f'pessoa{prefix}'))
                
                #chek pessoas
                registros_pessoas = []
                pessoas = []
                for pessoa in form_pessoas:
                    pessoa_check = check_pessoas(request,id_pessoa=pessoa['id_pessoa'].value())
                    if pessoa_check:
                        pessoa = update_pessoa(form_pessoa=pessoa,pessoa=pessoa_check) if pessoa_check else pessoa_check
                    else:
                        if pessoa.is_valid():
                            pessoa_save = pessoa.save()
                            pessoas.append(model_to_dict(pessoa_save))
                            print(pessoa_save)
                            registro_pessoa = ModelRegistrosPessoaspcepa(protocolo=registro,id_pessoa=pessoa_save)
                            registro_pessoa.save()
                            registros_pessoas.append(model_to_dict(registro_pessoa))
                        
                context = {
                    'registro':model_to_dict(registro),
                    'registro_pessoas':pessoas,
                    'registro_item':analises,
                    'registro_imagens':imagens,
                    'instituicao': ModelUsuarios.objects.get(id=request.user.id).instituicao,
                }

                return render(request, 'extrato.html', context)
            else:
                return HttpResponse('nao salvo')
            
@login_required
def pericia_veicular(request):
    template = 'analise.html'
    if request.method == 'GET':
        operacoes = ModelOperacoes.objects.filter(data_inicio__lte=datetime.datetime.now(),data_fim__gte=datetime.datetime.now())
        chefes = ModelUsuarios.objects.filter(comandante='True')
        form_registros = RegistrosPCEPAForm()
        form_imagem = ImagemForm(prefix='imagem1')
        form_pessoas = PessoasForm(prefix='pessoa1')
        try:
            instituicao = ModelUsuarios.objects.get(id=request.user.id).instituicao
        except:
            instituicao = 'NAO DEFINIDO'
        context = {'operacoes':operacoes,
                   'chefes': chefes,
                   'instituicao': instituicao,
                   'form_pessoa': form_pessoas,
                   'form_registros': form_registros,
                   'form_imagem': form_imagem,
                   }
        return render(request, template,context)
    # elif url_parameter:
    #     pessoa = ModelPessoas.objects.filter(nome_completo__icontains=url_parameter)
    #     if is_ajax_request:
    #         html = render_to_string(
    #             template_name="includes/resultados_pesquisa.html", 
    #             context={"resultados_pesquisa": pessoa}
    #         )

    #         data_dict = {"html_from_view": html}

    #         return JsonResponse(data=data_dict, safe=False)
    elif request.POST:
        form_registros = RegistrosPCEPAForm(request.POST)
        if request.POST.get('protocolo'):
            try:
                ModelRegistrospcepa.objects.get(protocolo=request.POST.get('protocolo'))
                return HttpResponse('Esse numero de prtocolo ja esta cadastrado')
            except: pass
            
            print(request.POST.get('imagem'))
            imagem = ModelImagens(imagem=request.POST.get('imagem'))
            imagem.save()
            analises = []
            if form_registros.is_valid():
                registro = ModelRegistrospcepa(protocolo=request.POST.get('protocolo'),caso=request.POST.get('caso'),bop_tombo=request.POST.get('bop_tombo'),tipo_exame=request.POST.get('tipo_exame'),data_exame=request.POST.get('data_exame'),id_usuario=ModelUsuarios.objects.get(id=request.user.id),id_operacao=ModelOperacoes.objects.get(id=request.POST.get('nome_op')),id_comandante=ModelUsuarios.objects.get(id=request.POST.get('chefe_guarnicao')))
                registro.save()
                
                # for prefix in range(1,len(request.POST.get('qtd_pessoas'))+1):
                for prefix in range(1,2):
                    
                    analise = AnaliseBalisticaForm(request.POST,prefix=f'analise{prefix}')
                    if analise.is_valid():
                        print(analise['tipo_material'].value())
                        analise = ModelAnaliseBalisticapcepa(protocolo=registro, tipo_material=analise['tipo_material'].value(), calibre=analise['calibre'].value(), nro_serie_rastreio=analise['nro_serie_rastreio'].value(), nro_patrimonio=analise['nro_patrimonio'].value(),qtd=analise['qtd'].value(),id_imagem=imagem)
                        analise.save()
                        analises.append(model_to_dict(analise))
                        
                form_pessoas = []
                # for prefix in range(1,len(request.POST.get('qtd_pessoas'))+2):
                for prefix in range(1,3):
                    form_pessoas.append(PessoasForm(request.POST,prefix=f'pessoa{prefix}'))
                
                #chek pessoas
                registros_pessoas = []
                pessoas = []
                for pessoa in form_pessoas:
                    pessoa_check = check_pessoas(request,id_pessoa=pessoa['id_pessoa'].value())
                    if pessoa_check:
                        pessoa = update_pessoa(form_pessoa=pessoa,pessoa=pessoa_check) if pessoa_check else pessoa_check
                    else:
                        if pessoa.is_valid():
                            pessoa_save = pessoa.save()
                            pessoas.append(model_to_dict(pessoa_save))
                            print(pessoa_save)
                            registro_pessoa = ModelRegistrosPessoaspcepa(protocolo=registro,id_pessoa=pessoa_save)
                            registro_pessoa.save()
                            registros_pessoas.append(model_to_dict(registro_pessoa))
                        
                context = {
                    'registro':model_to_dict(registro),
                    'registro_pessoas':pessoas,
                    'registro_item':analises,
                    'instituicao': ModelUsuarios.objects.get(id=request.user.id).instituicao,
                }

                return render(request, 'extrato.html', context)
            else:
                return HttpResponse('nao salvo')
