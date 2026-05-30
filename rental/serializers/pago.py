# rental/serializers/pago.py
from rest_framework import serializers
from rental.models import Pago, Alquiler, MetodoPago
from rental.serializers.alquiler import AlquilerSerializer
from rental.serializers.catalogo import MetodoPagoSerializer


class PagoSerializer(serializers.ModelSerializer):
    alquiler = AlquilerSerializer(read_only=True)
    alquiler_id = serializers.PrimaryKeyRelatedField(
        source='alquiler',
        write_only=True,
        queryset=Alquiler.objects.all(),
    )
    metodo_detalle = MetodoPagoSerializer(read_only=True)
    metodo_detalle_id = serializers.PrimaryKeyRelatedField(
        source='metodo_detalle',
        write_only=True,
        queryset=MetodoPago.objects.filter(is_active=True),
        required=False,
        allow_null=True,
    )

    class Meta:
        model  = Pago
        fields = [
            'id', 'alquiler', 'alquiler_id', 'monto',
            'metodo_pago', 'metodo_detalle', 'metodo_detalle_id',
            'fecha_pago', 'estado', 'referencia',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_monto(self, value):
        if value <= 0:
            raise serializers.ValidationError('Amount must be greater than 0.')
        return value

    def validate(self, data):
        # Si el estado es PAGADO, debe tener fecha de pago
        estado = data.get('estado', self.instance.estado if self.instance else 'PENDIENTE')
        fecha_pago = data.get('fecha_pago', self.instance.fecha_pago if self.instance else None)
        
        if estado == 'PAGADO' and not fecha_pago:
            data['fecha_pago'] = serializers.DateTimeField().to_representation(
                serializers.DateTimeField()
            )
        
        return data
