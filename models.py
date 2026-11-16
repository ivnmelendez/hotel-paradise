from django.db import models

class Habitacion(models.Model):
    TIPOS = [
        ('Individual', 'Individual'),
        ('Doble', 'Doble'),
        ('Suite', 'Suite'),
        ('Presidencial', 'Presidencial'),
    ]

    numero = models.IntegerField(unique=True)
    tipo = models.CharField(max_length=50, choices=TIPOS)
    precio_noche = models.DecimalField(max_digits=10, decimal_places=2)
    capacidad = models.IntegerField()
    disponible = models.BooleanField(default=True)
    imagen = models.ImageField(upload_to='habitaciones/', blank=True, null=True)

    def __str__(self):
        return f"Habitación {self.numero} - {self.tipo}"
