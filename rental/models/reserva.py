# rental/models/reserva.py
from django.db import models
from .cliente import Cliente
from .vehiculo import Vehiculo


class Reserva(models.Model):
    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('CONFIRMADA', 'Confirmada'),
        ('CANCELADA', 'Cancelada'),
        ('FINALIZADA', 'Finalizada'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name='reservas')
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.PROTECT, related_name='reservas')
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='PENDIENTE')
    observaciones = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Reserva'
        verbose_name_plural = 'Reservas'
        ordering = ['-created_at']

    def __str__(self):
        return f'Reerva #{self.id} - {self.vehiculo.placa} ({self.estado})'

    @property
    def dias(self):
        from datetime import datetime
        delta = self.fecha_fin - self.fecha_inicio
        return delta.days + 1

    @property
    def total_estimado(self):
        return self.dias * self.vehiculo.precio_dia
