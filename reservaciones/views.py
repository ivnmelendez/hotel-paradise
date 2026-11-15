from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from habitaciones.models import Habitacion
from .models import Reservacion
from .forms import ReservacionForm

@login_required
def lista_reservaciones(request):
    reservaciones = Reservacion.objects.all()

    cliente = request.GET.get('cliente')
    if cliente:
        reservaciones = reservaciones.filter(cliente__nombre__icontains=cliente) | reservaciones.filter(cliente__apellidos__icontains=cliente)

    habitacion = request.GET.get('habitacion')
    if habitacion:
        reservaciones = reservaciones.filter(habitacion__numero=habitacion)

    tipo = request.GET.get('tipo')
    if tipo:
        reservaciones = reservaciones.filter(habitacion__tipo=tipo)

    return render(request, 'reservaciones/lista.html', {
        'reservaciones': reservaciones,
        'buscar_cliente': cliente or '',
        'buscar_habitacion': habitacion or '',
        'buscar_tipo': tipo or '',
        'tipos_habitacion': Habitacion.TIPOS,
    })

@login_required
def crear_reservacion(request):
    if request.method == 'POST':
        form = ReservacionForm(request.POST)
        if form.is_valid():
            reserva = form.save(commit=False)
            noches = (reserva.fecha_salida - reserva.fecha_entrada).days
            reserva.total = noches * reserva.habitacion.precio_noche
            reserva.save()
            return redirect('lista_reservaciones')
    else:
        form = ReservacionForm()

    return render(request, 'reservaciones/formulario.html', {
        'form': form,
        'titulo': 'Nueva Reservación'
    })

@login_required
def editar_reservacion(request, id):
    reservacion = get_object_or_404(Reservacion, id=id)
    if request.method == 'POST':
        form = ReservacionForm(request.POST, instance=reservacion)
        if form.is_valid():
            reserva = form.save(commit=False)
            noches = (reserva.fecha_salida - reserva.fecha_entrada).days
            reserva.total = noches * reserva.habitacion.precio_noche
            reserva.save()
            return redirect('lista_reservaciones')
    else:
        form = ReservacionForm(instance=reservacion)

    return render(request, 'reservaciones/formulario.html', {
        'form': form,
        'titulo': 'Editar Reservación'
    })

@login_required
def cancelar_reservacion(request, id):
    reservacion = get_object_or_404(Reservacion, id=id)
    if request.method == 'POST':
        reservacion.estado = 'Cancelada'
        reservacion.save()
        return redirect('lista_reservaciones')

    return render(request, 'reservaciones/cancelar.html', {
        'reservacion': reservacion
    })

@login_required
def consultar_disponibilidad(request):
    fecha_entrada = request.GET.get('fecha_entrada')
    fecha_salida = request.GET.get('fecha_salida')
    tipo = request.GET.get('tipo')

    habitaciones_disponibles = None
    error_fechas = None

    if fecha_entrada and fecha_salida:
        if fecha_salida <= fecha_entrada:
            error_fechas = "La fecha de salida debe ser mayor que la fecha de entrada."
        else:
            ocupadas = Reservacion.objects.filter(
                estado='Activa',
                fecha_entrada__lt=fecha_salida,
                fecha_salida__gt=fecha_entrada
            ).values_list('habitacion_id', flat=True)

            habitaciones_disponibles = Habitacion.objects.filter(disponible=True).exclude(id__in=ocupadas)

            if tipo:
                habitaciones_disponibles = habitaciones_disponibles.filter(tipo=tipo)

    return render(request, 'reservaciones/disponibilidad.html', {
        'habitaciones_disponibles': habitaciones_disponibles,
        'fecha_entrada': fecha_entrada or '',
        'fecha_salida': fecha_salida or '',
        'tipo_seleccionado': tipo or '',
        'tipos_habitacion': Habitacion.TIPOS,
        'error_fechas': error_fechas,
    })
