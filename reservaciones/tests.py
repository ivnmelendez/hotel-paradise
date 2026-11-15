from django.test import TestCase
from datetime import date, timedelta
from habitaciones.models import Habitacion
from clientes.models import Cliente
from .models import Reservacion
from .forms import ReservacionForm

class ReservacionTests(TestCase):
    def setUp(self):
        self.habitacion = Habitacion.objects.create(
            numero=101,
            tipo='Individual',
            precio_noche=850,
            capacidad=1,
            disponible=True
        )
        self.cliente = Cliente.objects.create(
            nombre='Juan',
            apellidos='Perez',
            correo='juan@correo.com',
            telefono='5512345678'
        )

    def test_fecha_salida_menor_entrada(self):
        hoy = date.today()
        form = ReservacionForm(data={
            'cliente': self.cliente.id,
            'habitacion': self.habitacion.id,
            'fecha_entrada': hoy + timedelta(days=3),
            'fecha_salida': hoy + timedelta(days=1),
            'estado': 'Activa'
        })
        self.assertFalse(form.is_valid())

    def test_no_traslape_fechas(self):
        hoy = date.today()
        Reservacion.objects.create(
            cliente=self.cliente,
            habitacion=self.habitacion,
            fecha_entrada=hoy,
            fecha_salida=hoy + timedelta(days=3),
            total=2550,
            estado='Activa'
        )
        form = ReservacionForm(data={
            'cliente': self.cliente.id,
            'habitacion': self.habitacion.id,
            'fecha_entrada': hoy + timedelta(days=1),
            'fecha_salida': hoy + timedelta(days=4),
            'estado': 'Activa'
        })
        self.assertFalse(form.is_valid())
