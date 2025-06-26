from django.shortcuts import render, redirect
from .forms import RegistroUsuarioForm, ClienteForm
from django.contrib.auth import login

def registro(request):
    if request.method == 'POST':
        form_usuario = RegistroUsuarioForm(request.POST)
        form_cliente = ClienteForm(request.POST)

        if form_usuario.is_valid() and form_cliente.is_valid():
            user = form_usuario.save()
            cliente = form_cliente.save(commit=False)
            cliente.user = user
            cliente.save()
            login(request, user)
            return redirect('home')  # redireciona para a página inicial

    else:
        form_usuario = RegistroUsuarioForm()
        form_cliente = ClienteForm()

    return render(request, 'clientes/registro.html', {
        'form_usuario': form_usuario,
        'form_cliente': form_cliente,
    })
