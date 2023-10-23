from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name="login"),
    path('sair/', views.sair, name='sair'),
    path('', views.home, name='home'),
    path('cadastro/operacao/', views.cad_op, name='cad_op'),
    path('usuario/', views.usuario, name='usuario'),
    path('dashboard/', views.dashboard, name='dashboard'),
]