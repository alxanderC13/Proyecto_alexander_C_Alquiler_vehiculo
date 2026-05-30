# rental/serializers/cliente.py
from rest_framework import serializers
from rental.models import Cliente


class ClienteSerializer(serializers.ModelSerializer):
    nombre_completo = serializers.ReadOnlyField()
    num_reservas = serializers.SerializerMethodField()
    num_alquileres = serializers.SerializerMethodField()

    class Meta:
        model  = Cliente
        fields = [
            'id', 'nombres', 'apellidos', 'cedula', 'licencia_conducir',
            'telefono', 'direccion', 'email', 'estado',
            'nombre_completo', 'num_reservas', 'num_alquileres',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_num_reservas(self, obj):
        return obj.reservas.count()

    def get_num_alquileres(self, obj):
        return obj.alquileres.count()

    def validate_cedula(self, value):
        qs = Cliente.objects.filter(cedula=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError('A client with this ID already exists.')
        return value

    def validate_licencia_conducir(self, value):
        qs = Cliente.objects.filter(licencia_conducir=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError('A client with this driver license already exists.')
        return value

    def validate_email(self, value):
        qs = Cliente.objects.filter(email=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError('A client with this email already exists.')
        return value
