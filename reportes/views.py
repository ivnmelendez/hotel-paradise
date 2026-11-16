from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count
from habitaciones.models import Habitacion
from clientes.models import Cliente
from reservaciones.models import Reservacion

def login_usuario(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        usuario = authenticate(request, username=username, password=password)

        if usuario is not None:
            login(request, usuario)
            return redirect('dashboard')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')

    return render(request, 'reportes/login.html')

@login_required
def logout_usuario(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    total_clientes = Cliente.objects.count()
    total_habitaciones = Habitacion.objects.count()
    total_reservaciones = Reservacion.objects.count()
    habitaciones_disponibles = Habitacion.objects.filter(disponible=True).count()

    ingresos = Reservacion.objects.filter(estado='Activa').aggregate(Sum('total'))['total__sum']
    if ingresos is None:
        ingresos = 0

    ultimas_reservaciones = Reservacion.objects.all().order_by('-id')[:5]

    return render(request, 'interfaz/dashboard.html', {
        'total_clientes': total_clientes,
        'total_habitaciones': total_habitaciones,
        'total_reservaciones': total_reservaciones,
        'habitaciones_disponibles': habitaciones_disponibles,
        'ingresos_generados': ingresos,
        'ultimas_reservaciones': ultimas_reservaciones,
    })

@login_required
def reportes_estadisticas(request):
    reservas_activas = Reservacion.objects.filter(estado='Activa').count()
    reservas_canceladas = Reservacion.objects.filter(estado='Cancelada').count()

    ingresos = Reservacion.objects.filter(estado='Activa').aggregate(Sum('total'))['total__sum']
    if ingresos is None:
        ingresos = 0

    reporte_por_tipo = Reservacion.objects.filter(estado='Activa').values('habitacion__tipo').annotate(
        total_reservas=Count('id'),
        ingresos=Sum('total')
    )

    mejores_clientes = Cliente.objects.annotate(
        num_reservas=Count('reservacion')
    ).order_by('-num_reservas')[:5]

    return render(request, 'reportes/reportes.html', {
        'reservas_activas': reservas_activas,
        'reservas_canceladas': reservas_canceladas,
        'ingresos_totales': ingresos,
        'reporte_por_tipo': reporte_por_tipo,
        'mejores_clientes': mejores_clientes,
    })
