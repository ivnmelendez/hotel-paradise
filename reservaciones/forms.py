from django import forms
from .models import Reservacion

class ReservacionForm(forms.ModelForm):
    class Meta:
        model = Reservacion
        fields = ['cliente', 'habitacion', 'fecha_entrada', 'fecha_salida', 'estado']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-select'}),
            'habitacion': forms.Select(attrs={'class': 'form-select'}),
            'fecha_entrada': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_salida': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        habitacion = cleaned_data.get('habitacion')
        fecha_entrada = cleaned_data.get('fecha_entrada')
        fecha_salida = cleaned_data.get('fecha_salida')
        estado = cleaned_data.get('estado')

        if fecha_entrada and fecha_salida:
            if fecha_salida <= fecha_entrada:
                raise forms.ValidationError("La fecha de salida debe ser mayor que la fecha de entrada.")

            if habitacion and estado == 'Activa':
                traslapes = Reservacion.objects.filter(
                    habitacion=habitacion,
                    estado='Activa',
                    fecha_entrada__lt=fecha_salida,
                    fecha_salida__gt=fecha_entrada
                )
                if self.instance.id:
                    traslapes = traslapes.exclude(id=self.instance.id)

                if traslapes.exists():
                    raise forms.ValidationError("Esta habitación ya está reservada en esas fechas.")

        return cleaned_data
