# rental/models/vehiculo.py
from django.db import models
from .catalogo import CategoriaVehiculo


class Vehiculo(models.Model):
    CATEGORIA_CHOICES = [
        ('ECONOMICO', 'Económico'),
        ('SUV', 'SUV'),
        ('SEDAN', 'Sedán'),
        ('CAMIONETA', 'Camioneta'),
        ('LUJO', 'Lujo'),
    ]

    ESTADO_CHOICES = [
        ('DISPONIBLE', 'Disponible'),
        ('ALQUILADO', 'Alquilado'),
        ('MANTENIMIENTO', 'Mantenimiento'),
        ('FUERA_SERVICIO', 'Fuera de Servicio'),
    ]

    placa = models.CharField(max_length=20, unique=True)
    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    anio = models.PositiveIntegerField()
    color = models.CharField(max_length=50)
    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES)
    categoria_detalle = models.ForeignKey(
        CategoriaVehiculo,
        on_delete=models.PROTECT,
        related_name='vehiculos',
        null=True,
        blank=True,
    )
    precio_dia = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='DISPONIBLE')
    kilometraje = models.PositiveIntegerField(default=0)
    disponible = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Vehículo'
        verbose_name_plural = 'Vehículos'
        ordering = ['marca', 'modelo']

    def __str__(self):
        return f'{self.marca} {self.modelo} ({self.placa})'

    @property
    def esta_disponible(self):
        return self.disponible and self.estado == 'DISPONIBLE'
