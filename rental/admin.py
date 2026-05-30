# rental/admin.py
from django.contrib import admin
from rental.models import (
    Usuario, CategoriaVehiculo, TipoMantenimiento, MetodoPago,
    Cliente, Vehiculo, Reserva, Alquiler, Pago, Mantenimiento,
)


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display  = ['id', 'username', 'email', 'rol', 'estado', 'is_staff', 'is_active', 'date_joined']
    list_filter   = ['rol', 'estado', 'is_staff', 'is_active']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    list_editable = ['estado', 'is_staff', 'is_active']


@admin.register(CategoriaVehiculo)
class CategoriaVehiculoAdmin(admin.ModelAdmin):
    list_display  = ['id', 'nombre', 'is_active', 'created_at']
    list_filter   = ['is_active']
    search_fields = ['nombre']


@admin.register(TipoMantenimiento)
class TipoMantenimientoAdmin(admin.ModelAdmin):
    list_display  = ['id', 'nombre', 'is_active', 'created_at']
    list_filter   = ['is_active']
    search_fields = ['nombre']


@admin.register(MetodoPago)
class MetodoPagoAdmin(admin.ModelAdmin):
    list_display  = ['id', 'nombre', 'is_active', 'created_at']
    list_filter   = ['is_active']
    search_fields = ['nombre']


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display  = ['id', 'nombres', 'apellidos', 'cedula', 'email', 'estado', 'created_at']
    list_filter   = ['estado']
    search_fields = ['nombres', 'apellidos', 'cedula', 'email']
    list_editable = ['estado']


@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
    list_display  = ['id', 'placa', 'marca', 'modelo', 'anio', 'categoria', 'precio_dia', 'estado', 'disponible']
    list_filter   = ['categoria', 'estado', 'disponible']
    search_fields = ['placa', 'marca', 'modelo']
    list_editable = ['precio_dia', 'estado', 'disponible']


@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display    = ['id', 'cliente', 'vehiculo', 'fecha_inicio', 'fecha_fin', 'estado', 'created_at']
    list_filter     = ['estado']
    search_fields   = ['cliente__nombres', 'cliente__apellidos', 'vehiculo__placa']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Alquiler)
class AlquilerAdmin(admin.ModelAdmin):
    list_display    = ['id', 'codigo_alquiler', 'cliente', 'vehiculo', 'fecha_inicio', 'fecha_fin', 'estado', 'total']
    list_filter     = ['estado']
    search_fields   = ['codigo_alquiler', 'cliente__nombres', 'cliente__apellidos', 'vehiculo__placa']
    readonly_fields = ['codigo_alquiler', 'created_at', 'updated_at']


@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display    = ['id', 'alquiler', 'monto', 'metodo_pago', 'estado', 'fecha_pago']
    list_filter     = ['estado', 'metodo_pago']
    search_fields   = ['alquiler__codigo_alquiler', 'referencia']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Mantenimiento)
class MantenimientoAdmin(admin.ModelAdmin):
    list_display    = ['id', 'vehiculo', 'tipo_mantenimiento', 'fecha_inicio', 'fecha_fin', 'estado', 'costo']
    list_filter     = ['estado']
    search_fields   = ['vehiculo__placa', 'tipo_mantenimiento', 'descripcion']
    readonly_fields = ['created_at', 'updated_at']