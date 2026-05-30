# rental/models/cliente.py
from django.db import models


class Cliente(models.Model):
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    cedula = models.CharField(max_length=20, unique=True)
    licencia_conducir = models.CharField(max_length=50, unique=True)
    telefono = models.CharField(max_length=20)
    direccion = models.TextField()
    email = models.EmailField()
    estado = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['apellidos', 'nombres']

    def __str__(self):
        return f'{self.nombres} {self.apellidos} ({self.cedula})'

    @property
    def nombre_completo(self):
        return f'{self.nombres} {self.apellidos}'
