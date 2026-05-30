# rental/models/mantenimiento.py
from django.db import models
from .vehiculo import Vehiculo
from .catalogo import TipoMantenimiento


class Mantenimiento(models.Model):
    ESTADO_CHOICES = [
        ('PROGRAMADO', 'Programado'),
        ('EN_PROCESO', 'En Proceso'),
        ('COMPLETADO', 'Completado'),
        ('CANCELADO', 'Cancelado'),
    ]

    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.PROTECT, related_name='mantenimientos')
    tipo_mantenimiento = models.CharField(max_length=50)
    tipo_detalle = models.ForeignKey(
        TipoMantenimiento,
        on_delete=models.PROTECT,
        related_name='mantenimientos',
        null=True,
        blank=True,
    )
    descripcion = models.TextField()
    costo = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='PROGRAMADO')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Mantenimiento'
        verbose_name_plural = 'Mantenimientos'
        ordering = ['-created_at']

    def __str__(self):
        return f'Mantenimiento #{self.id} - {self.vehiculo.placa} ({self.estado})'
