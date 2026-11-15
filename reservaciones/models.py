from django.db import models
from clientes.models import Cliente
from habitaciones.models import Habitacion

class Reservacion(models.Model):
    ESTADOS = [
        ('Activa', 'Activa'),
        ('Cancelada', 'Cancelada'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    habitacion = models.ForeignKey(Habitacion, on_delete=models.CASCADE)
    fecha_entrada = models.DateField()
    fecha_salida = models.DateField()
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='Activa')

    def __str__(self):
        return f"Reservación {self.id} - Habitación {self.habitacion.numero}"
