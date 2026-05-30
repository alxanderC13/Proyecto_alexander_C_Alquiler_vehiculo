# rental/models/__init__.py
from .user import Usuario
from .catalogo import CategoriaVehiculo, TipoMantenimiento, MetodoPago
from .cliente import Cliente
from .vehiculo import Vehiculo
from .reserva import Reserva
from .alquiler import Alquiler
from .pago import Pago
from .mantenimiento import Mantenimiento

__all__ = [
    'Usuario',
    'CategoriaVehiculo',
    'TipoMantenimiento',
    'MetodoPago',
    'Cliente',
    'Vehiculo',
    'Reserva',
    'Alquiler',
    'Pago',
    'Mantenimiento',
]