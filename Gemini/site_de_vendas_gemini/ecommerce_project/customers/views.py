# customers/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, CustomerProfileForm, UserUpdateForm
from .models import CustomerProfile # Importar para criar o perfil após o registro

def register_view(request):
    """
    View para registro de novos usuários.
    """
    if request.user.is_authenticated:
        messages.info(request, "Você já está logado.")
        return redirect('home')

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Cria um perfil de cliente para o novo usuário
            CustomerProfile.objects.create(user=user)
            messages.success(request, f'Sua conta foi criada com sucesso! Agora você pode fazer login.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'customers/register.html', {'form': form})

@login_required
def customer_dashboard_view(request):
    """
    Exibe o painel do cliente com informações do perfil e pedidos.
    """
    # Você precisará buscar os pedidos do usuário aqui
    # from orders.models import Order (importar no topo do arquivo se usar)
    # user_orders = Order.objects.filter(customer=request.user).order_by('-created_at')

    context = {
        # 'user_orders': user_orders,
    }
    return render(request, 'customers/customer_dashboard.html', context)

@login_required
def customer_profile_edit_view(request):
    """
    Permite ao cliente editar seu perfil.
    """
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = CustomerProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Seu perfil foi atualizado com sucesso!')
            return redirect('customer_dashboard')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = CustomerProfileForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'customers/customer_profile_edit.html', context)