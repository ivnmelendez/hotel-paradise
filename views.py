from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Habitacion
from .forms import HabitacionForm

@login_required
def lista_habitaciones(request):
    habitaciones = Habitacion.objects.all()

    numero = request.GET.get('numero')
    if numero:
        habitaciones = habitaciones.filter(numero=numero)

    tipo = request.GET.get('tipo')
    if tipo:
        habitaciones = habitaciones.filter(tipo=tipo)

    return render(request, 'habitaciones/lista.html', {
        'habitaciones': habitaciones,
        'buscar_numero': numero or '',
        'buscar_tipo': tipo or '',
        'tipos_habitacion': Habitacion.TIPOS,
    })

@login_required
def crear_habitacion(request):
    if request.method == 'POST':
        form = HabitacionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('lista_habitaciones')
    else:
        form = HabitacionForm()

    return render(request, 'habitaciones/formulario.html', {
        'form': form,
        'titulo': 'Nueva Habitación'
    })

@login_required
def editar_habitacion(request, id):
    habitacion = get_object_or_404(Habitacion, id=id)
    if request.method == 'POST':
        form = HabitacionForm(request.POST, request.FILES, instance=habitacion)
        if form.is_valid():
            form.save()
            return redirect('lista_habitaciones')
    else:
        form = HabitacionForm(instance=habitacion)

    return render(request, 'habitaciones/formulario.html', {
        'form': form,
        'titulo': 'Editar Habitación'
    })

@login_required
def eliminar_habitacion(request, id):
    habitacion = get_object_or_404(Habitacion, id=id)
    tiene_reservas_activas = habitacion.reservacion_set.filter(estado='Activa').exists()

    if request.method == 'POST':
        if tiene_reservas_activas:
            messages.error(request, 'No se puede eliminar una habitación con reservaciones activas.')
            return redirect('lista_habitaciones')
        habitacion.delete()
        return redirect('lista_habitaciones')

    return render(request, 'habitaciones/eliminar.html', {
        'habitacion': habitacion,
        'tiene_reservas_activas': tiene_reservas_activas
    })
