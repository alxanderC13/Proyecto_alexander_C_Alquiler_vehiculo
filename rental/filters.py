# rental/filters.py
import django_filters
from rental.models import (
    Usuario, CategoriaVehiculo, TipoMantenimiento, MetodoPago,
    Cliente, Vehiculo, Reserva, Alquiler, Pago, Mantenimiento,
)


class UsuarioFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(lookup_expr='icontains')
    email = django_filters.CharFilter(lookup_expr='icontains')
    rol = django_filters.CharFilter()

    class Meta:
        model  = Usuario
        fields = ['rol', 'estado', 'is_staff', 'is_active']


class CategoriaVehiculoFilter(django_filters.FilterSet):
    nombre = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model  = CategoriaVehiculo
        fields = ['is_active']


class TipoMantenimientoFilter(django_filters.FilterSet):
    nombre = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model  = TipoMantenimiento
        fields = ['is_active']


class MetodoPagoFilter(django_filters.FilterSet):
    nombre = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model  = MetodoPago
        fields = ['is_active']


class ClienteFilter(django_filters.FilterSet):
    nombres = django_filters.CharFilter(lookup_expr='icontains')
    apellidos = django_filters.CharFilter(lookup_expr='icontains')
    cedula = django_filters.CharFilter(lookup_expr='icontains')
    email = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model  = Cliente
        fields = ['estado']


class VehiculoFilter(django_filters.FilterSet):
    marca = django_filters.CharFilter(lookup_expr='icontains')
    modelo = django_filters.CharFilter(lookup_expr='icontains')
    placa = django_filters.CharFilter(lookup_expr='icontains')
    precio_min = django_filters.NumberFilter(field_name='precio_dia', lookup_expr='gte')
    precio_max = django_filters.NumberFilter(field_name='precio_dia', lookup_expr='lte')
    anio_min = django_filters.NumberFilter(field_name='anio', lookup_expr='gte')
    anio_max = django_filters.NumberFilter(field_name='anio', lookup_expr='lte')
    categoria = django_filters.CharFilter()

    class Meta:
        model  = Vehiculo
        fields = ['categoria', 'estado', 'disponible']


class ReservaFilter(django_filters.FilterSet):
    from_date = django_filters.DateFilter(field_name='fecha_inicio', lookup_expr='gte')
    to_date = django_filters.DateFilter(field_name='fecha_fin', lookup_expr='lte')
    created_from = django_filters.DateFilter(field_name='created_at', lookup_expr='date__gte')
    created_to = django_filters.DateFilter(field_name='created_at', lookup_expr='date__lte')

    class Meta:
        model  = Reserva
        fields = ['estado', 'cliente', 'vehiculo']


class AlquilerFilter(django_filters.FilterSet):
    from_date = django_filters.DateFilter(field_name='fecha_inicio', lookup_expr='gte')
    to_date = django_filters.DateFilter(field_name='fecha_fin', lookup_expr='lte')
    created_from = django_filters.DateFilter(field_name='created_at', lookup_expr='date__gte')
    created_to = django_filters.DateFilter(field_name='created_at', lookup_expr='date__lte')
    codigo = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model  = Alquiler
        fields = ['estado', 'cliente', 'vehiculo', 'usuario_responsable']


class PagoFilter(django_filters.FilterSet):
    from_date = django_filters.DateFilter(field_name='fecha_pago', lookup_expr='date__gte')
    to_date = django_filters.DateFilter(field_name='fecha_pago', lookup_expr='date__lte')
    created_from = django_filters.DateFilter(field_name='created_at', lookup_expr='date__gte')
    created_to = django_filters.DateFilter(field_name='created_at', lookup_expr='date__lte')
    monto_min = django_filters.NumberFilter(field_name='monto', lookup_expr='gte')
    monto_max = django_filters.NumberFilter(field_name='monto', lookup_expr='lte')

    class Meta:
        model  = Pago
        fields = ['estado', 'metodo_pago', 'alquiler']


class MantenimientoFilter(django_filters.FilterSet):
    from_date = django_filters.DateFilter(field_name='fecha_inicio', lookup_expr='gte')
    to_date = django_filters.DateFilter(field_name='fecha_fin', lookup_expr='lte')
    created_from = django_filters.DateFilter(field_name='created_at', lookup_expr='date__gte')
    created_to = django_filters.DateFilter(field_name='created_at', lookup_expr='date__lte')
    costo_min = django_filters.NumberFilter(field_name='costo', lookup_expr='gte')
    costo_max = django_filters.NumberFilter(field_name='costo', lookup_expr='lte')

    class Meta:
        model  = Mantenimiento
        fields = ['estado', 'vehiculo']