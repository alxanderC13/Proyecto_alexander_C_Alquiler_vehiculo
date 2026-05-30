# rental/serializers/alquiler.py
from rest_framework import serializers
from rental.models import Alquiler, Cliente, Vehiculo, Reserva, Usuario
from rental.serializers.cliente import ClienteSerializer
from rental.serializers.vehiculo import VehiculoSummarySerializer
from rental.serializers.reserva import ReservaSerializer


class AlquilerSerializer(serializers.ModelSerializer):
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
        queryset=Vehiculo.objects.all(),
    )
    reserva = ReservaSerializer(read_only=True)
    reserva_id = serializers.PrimaryKeyRelatedField(
        source='reserva',
        write_only=True,
        queryset=Reserva.objects.all(),
        required=False,
        allow_null=True,
    )
    usuario_responsable_nombre = serializers.CharField(source='usuario_responsable.username', read_only=True)
    dias = serializers.ReadOnlyField()

    class Meta:
        model  = Alquiler
        fields = [
            'id', 'codigo_alquiler', 'cliente', 'cliente_id',
            'vehiculo', 'vehiculo_id', 'reserva', 'reserva_id',
            'fecha_inicio', 'fecha_fin', 'fecha_devolucion',
            'valor_dia', 'total', 'estado', 'observaciones',
            'usuario_responsable', 'usuario_responsable_nombre',
            'dias', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate(self, data):
        # Validar que el vehículo esté disponible
        vehiculo = data.get('vehiculo')
        if vehiculo and vehiculo.estado in ['MANTENIMIENTO', 'FUERA_SERVICIO']:
            raise serializers.ValidationError(
                'Cannot rent a vehicle that is in maintenance or out of service.'
            )
        
        # Validar que el vehículo no tenga alquileres activos
        if vehiculo:
            from django.db.models import Q
            alquileres_activos = Alquiler.objects.filter(
                vehiculo=vehiculo,
                estado='ACTIVO',
            )
            
            if self.instance:
                alquileres_activos = alquileres_activos.exclude(pk=self.instance.pk)
            
            if alquileres_activos.exists():
                raise serializers.ValidationError(
                    'The vehicle already has an active rental.'
                )
        
        return data

    def create(self, validated_data):
        # Generar código de alquiler automático
        from datetime import datetime
        year = datetime.now().year
        last_alquiler = Alquiler.objects.filter(codigo_alquiler__startswith=f'ALQ-{year}').order_by('-codigo_alquiler').first()
        if last_alquiler:
            last_num = int(last_alquiler.codigo_alquiler.split('-')[-1])
            new_num = last_num + 1
        else:
            new_num = 1
        validated_data['codigo_alquiler'] = f'ALQ-{year}-{new_num:06d}'
        
        # Calcular total automáticamente
        alquiler = super().create(validated_data)
        alquiler.calcular_total()
        return alquiler
