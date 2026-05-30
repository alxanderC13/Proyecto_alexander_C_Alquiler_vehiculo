# rental/serializers/catalogo.py
from rest_framework import serializers
from rental.models import CategoriaVehiculo, TipoMantenimiento, MetodoPago


class CategoriaVehiculoSerializer(serializers.ModelSerializer):
    num_vehiculos = serializers.SerializerMethodField()

    class Meta:
        model  = CategoriaVehiculo
        fields = ['id', 'nombre', 'descripcion', 'is_active', 'num_vehiculos', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_num_vehiculos(self, obj):
        return obj.vehiculos.filter(disponible=True).count()


class TipoMantenimientoSerializer(serializers.ModelSerializer):
    num_mantenimientos = serializers.SerializerMethodField()

    class Meta:
        model  = TipoMantenimiento
        fields = ['id', 'nombre', 'descripcion', 'is_active', 'num_mantenimientos', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_num_mantenimientos(self, obj):
        return obj.mantenimientos.count()


class MetodoPagoSerializer(serializers.ModelSerializer):
    num_pagos = serializers.SerializerMethodField()

    class Meta:
        model  = MetodoPago
        fields = ['id', 'nombre', 'descripcion', 'is_active', 'num_pagos', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_num_pagos(self, obj):
        return obj.pagos.count()
