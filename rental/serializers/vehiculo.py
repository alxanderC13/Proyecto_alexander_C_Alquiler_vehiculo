# rental/serializers/vehiculo.py
from rest_framework import serializers
from rental.models import Vehiculo, CategoriaVehiculo
from rental.serializers.catalogo import CategoriaVehiculoSerializer


class VehiculoSerializer(serializers.ModelSerializer):
    categoria_detalle = CategoriaVehiculoSerializer(read_only=True)
    categoria_detalle_id = serializers.PrimaryKeyRelatedField(
        source='categoria_detalle',
        write_only=True,
        queryset=CategoriaVehiculo.objects.filter(is_active=True),
        required=False,
        allow_null=True,
    )
    esta_disponible = serializers.ReadOnlyField()

    class Meta:
        model  = Vehiculo
        fields = [
            'id', 'placa', 'marca', 'modelo', 'anio', 'color',
            'categoria', 'categoria_detalle', 'categoria_detalle_id',
            'precio_dia', 'estado', 'kilometraje', 'disponible',
            'esta_disponible', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_precio_dia(self, value):
        if value <= 0:
            raise serializers.ValidationError('Price per day must be greater than 0.')
        return value

    def validate_anio(self, value):
        from datetime import datetime
        current_year = datetime.now().year
        if value < 1900 or value > current_year + 1:
            raise serializers.ValidationError(f'Year must be between 1900 and {current_year + 1}.')
        return value

    def validate_kilometraje(self, value):
        if value < 0:
            raise serializers.ValidationError('Mileage cannot be negative.')
        return value


class VehiculoSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model  = Vehiculo
        fields = ['id', 'placa', 'marca', 'modelo', 'anio', 'precio_dia', 'estado', 'disponible']
