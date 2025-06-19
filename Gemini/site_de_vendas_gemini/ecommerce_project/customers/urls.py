# customers/urls.py

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views # Importa as views de autenticação do Django

urlpatterns = [
    # Autenticação
    path('login/', auth_views.LoginView.as_view(template_name='customers/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('cadastro/', views.register_view, name='register'),
    path('perfil/', views.customer_dashboard_view, name='customer_dashboard'),
    path('perfil/editar/', views.customer_profile_edit_view, name='customer_profile_edit'),

    # Recuperação de senha
    path('resetar_senha/', auth_views.PasswordResetView.as_view(template_name='customers/password_reset.html'), name='password_reset'),
    path('resetar_senha/enviado/', auth_views.PasswordResetDoneView.as_view(template_name='customers/password_reset_done.html'), name='password_reset_done'),
    path('resetar/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='customers/password_reset_confirm.html'), name='password_reset_confirm'),
    path('resetar_senha/completo/', auth_views.PasswordResetCompleteView.as_view(template_name='customers/password_reset_complete.html'), name='password_reset_complete'),
]