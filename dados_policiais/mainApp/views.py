from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required

@login_required
def sair(request):
    template = 'login'
    logout(request)
    return redirect(reverse_lazy(template))

@login_required
def home(request):
    template = 'home.html'
    context = {}
    return render(request, template, context)

@login_required
def usuario(request):
    template = 'usuario.html'
    context = {}
    return render(request, template, context)

@login_required
def dashboard(request):
    template = 'dashboard.html'
    context = {}
    return render(request, template, context)

@login_required
def cad_op(request):
    template = 'cadastro_operacao.html'
    context = {}
    return render(request, template, context)