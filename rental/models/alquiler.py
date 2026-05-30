# rental/models/alquiler.py
from django.db import models
from .user import Usuario
from .cliente import Cliente
from .vehiculo import Vehiculo
from .reserva import Reserva


class Alquiler(models.Model):
    ESTADO_CHOICES = [
        ('ACTIVO', 'Activo'),
        ('FINALIZADO', 'Finalizado'),
        ('ATRASADO', 'Atrasado'),
        ('CANCELADO', 'Cancelado'),
    ]

    codigo_alquiler = models.CharField(max_length=50, unique=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name='alquileres')
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.PROTECT, related_name='alquileres')
    reserva = models.ForeignKey(Reserva, on_delete=models.SET_NULL, related_name='alquileres', null=True, blank=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    fecha_devolucion = models.DateField(null=True, blank=True)
    valor_dia = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='ACTIVO')
    observaciones = models.TextField(blank=True, default='')
    usuario_responsable = models.ForeignKey(Usuario, on_delete=models.PROTECT, related_name='alquileres_asignados')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Alquiler'
        verbose_name_plural = 'Alquileres'
        ordering = ['-created_at']

    def __str__(self):
        return f'Alquiler {self.codigo_alquiler} - {self.vehiculo.placa} ({self.estado})'

    @property
    def dias(self):
        from datetime import datetime
        if self.fecha_devolucion:
            delta = self.fecha_devolucion - self.fecha_inicio
        else:
            delta = self.fecha_fin - self.fecha_inicio
        return delta.days + 1

    def calcular_total(self):
        self.total = self.dias * self.valor_dia
        self.save(update_fields=['total'])
