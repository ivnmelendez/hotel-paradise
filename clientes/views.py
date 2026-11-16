from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Cliente
from .forms import ClienteForm

@login_required
def lista_clientes(request):
    clientes = Cliente.objects.all()

    buscar = request.GET.get('q')
    if buscar:
        clientes = clientes.filter(nombre__icontains=buscar) | clientes.filter(apellidos__icontains=buscar) | clientes.filter(correo__icontains=buscar)

    return render(request, 'clientes/lista.html', {
        'clientes': clientes,
        'buscar': buscar or '',
    })

@login_required
def crear_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_clientes')
    else:
        form = ClienteForm()

    return render(request, 'clientes/formulario.html', {
        'form': form,
        'titulo': 'Nuevo Cliente'
    })

@login_required
def editar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('lista_clientes')
    else:
        form = ClienteForm(instance=cliente)

    return render(request, 'clientes/formulario.html', {
        'form': form,
        'titulo': 'Editar Cliente'
    })

@login_required
def eliminar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    if request.method == 'POST':
        cliente.delete()
        return redirect('lista_clientes')

    return render(request, 'clientes/eliminar.html', {
        'cliente': cliente
    })
