# rental/serializers/reserva.py
from rest_framework import serializers
from rental.models import Reserva, Cliente, Vehiculo
from rental.serializers.cliente import ClienteSerializer
from rental.serializers.vehiculo import VehiculoSummarySerializer


class ReservaSerializer(serializers.ModelSerializer):
    cliente = ClienteSerializer(read_only=True)
    cliente_id = serializers.PrimaryKeyRelatedField(
        source='cliente',
        write_only=True,
        queryset=Cliente.objects.filter(estado=True),
    )
    vehiculo = VehiculoSummarySerializer(read_only=True)
    vehiculo_id = serializers.PrimaryKeyRelatedField(
        source='vehiculo',
        write_only=True,
        queryset=Vehiculo.objects.filter(disponible=True),
    )
    dias = serializers.ReadOnlyField()
    total_estimado = serializers.ReadOnlyField()

    class Meta:
        model  = Reserva
        fields = [
            'id', 'cliente', 'cliente_id', 'vehiculo', 'vehiculo_id',
            'fecha_inicio', 'fecha_fin', 'estado', 'observaciones',
            'dias', 'total_estimado', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate(self, data):
        fecha_inicio = data.get('fecha_inicio')
        fecha_fin = data.get('fecha_fin')
        
        if fecha_inicio and fecha_fin:
            if fecha_fin <= fecha_inicio:
                raise serializers.ValidationError('End date must be after start date.')
            
            # Validar que el vehículo no tenga reservas o alquileres en el rango de fechas
            vehiculo = data.get('vehiculo')
            if vehiculo:
                from django.db.models import Q
                conflictos = Reserva.objects.filter(
                    vehiculo=vehiculo,
                    estado__in=['PENDIENTE', 'CONFIRMADA'],
                ).filter(
                    Q(fecha_inicio__lte=fecha_fin) & Q(fecha_fin__gte=fecha_inicio)
                )
                
                if self.instance:
                    conflictos = conflictos.exclude(pk=self.instance.pk)
                
                if conflictos.exists():
                    raise serializers.ValidationError(
                        'The vehicle already has a reservation for this date range.'
                    )
        
        return data
