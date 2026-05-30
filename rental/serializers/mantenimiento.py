# rental/serializers/mantenimiento.py
from rest_framework import serializers
from rental.models import Mantenimiento, Vehiculo, TipoMantenimiento
from rental.serializers.vehiculo import VehiculoSummarySerializer
from rental.serializers.catalogo import TipoMantenimientoSerializer


class MantenimientoSerializer(serializers.ModelSerializer):
    vehiculo = VehiculoSummarySerializer(read_only=True)
    vehiculo_id = serializers.PrimaryKeyRelatedField(
        source='vehiculo',
        write_only=True,
        queryset=Vehiculo.objects.all(),
    )
    tipo_detalle = TipoMantenimientoSerializer(read_only=True)
    tipo_detalle_id = serializers.PrimaryKeyRelatedField(
        source='tipo_detalle',
        write_only=True,
        queryset=TipoMantenimiento.objects.filter(is_active=True),
        required=False,
        allow_null=True,
    )

    class Meta:
        model  = Mantenimiento
        fields = [
            'id', 'vehiculo', 'vehiculo_id',
            'tipo_mantenimiento', 'tipo_detalle', 'tipo_detalle_id',
            'descripcion', 'costo',
            'fecha_inicio', 'fecha_fin', 'estado',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_costo(self, value):
        if value < 0:
            raise serializers.ValidationError('Cost cannot be negative.')
        return value

    def validate(self, data):
        fecha_inicio = data.get('fecha_inicio')
        fecha_fin = data.get('fecha_fin')
        
        if fecha_inicio and fecha_fin:
            if fecha_fin < fecha_inicio:
                raise serializers.ValidationError('End date cannot be before start date.')
        
        return data
