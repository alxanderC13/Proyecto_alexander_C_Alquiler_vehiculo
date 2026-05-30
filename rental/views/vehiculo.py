# rental/views/vehiculo.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg, Max, Min, Sum, Count

from rental.models import Vehiculo
from rental.serializers.vehiculo import VehiculoSerializer, VehiculoSummarySerializer
from rental.permissions import IsStaffOrReadOnly
from rental.filters import VehiculoFilter
from rental.pagination import StandardPagination


class VehiculoViewSet(viewsets.ModelViewSet):
    queryset           = Vehiculo.objects.select_related('categoria_detalle').all()
    serializer_class   = VehiculoSerializer
    permission_classes = [IsStaffOrReadOnly]
    pagination_class   = StandardPagination
    filter_backends    = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class    = VehiculoFilter
    search_fields      = ['marca', 'modelo', 'placa']
    ordering_fields    = ['marca', 'modelo', 'precio_dia', 'anio', 'created_at']
    ordering           = ['marca', 'modelo']

    @action(
        detail=True,
        methods=['post'],
        permission_classes=[IsAdminUser],
        url_path='actualizar-kilometraje',
    )
    def actualizar_kilometraje(self, request, pk=None):
        vehiculo = self.get_object()
        try:
            kilometraje = int(request.data.get('kilometraje', 0))
            if kilometraje < 0:
                raise ValueError
        except (ValueError, TypeError):
            return Response(
                {'error': 'Kilometraje must be a non-negative integer.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        vehiculo.kilometraje = kilometraje
        vehiculo.save(update_fields=['kilometraje'])
        return Response({
            'id': vehiculo.id,
            'placa': vehiculo.placa,
            'nuevo_kilometraje': vehiculo.kilometraje,
        })

    @action(
        detail=False,
        methods=['get'],
        permission_classes=[AllowAny],
        url_path='disponibles',
    )
    def disponibles(self, request):
        qs = self.filter_queryset(
            self.get_queryset().filter(estado='DISPONIBLE', disponible=True)
        )
        page = self.paginate_queryset(qs)
        if page is not None:
            return self.get_paginated_response(
                VehiculoSummarySerializer(page, many=True).data
            )
        return Response(VehiculoSummarySerializer(qs, many=True).data)

    @action(
        detail=False,
        methods=['get'],
        url_path='stats',
    )
    def stats(self, request):
        qs = Vehiculo.objects.all()
        data = qs.aggregate(
            total = Count('id'),
            avg_precio = Avg('precio_dia'),
            max_precio = Max('precio_dia'),
            min_precio = Min('precio_dia'),
            total_kilometraje = Sum('kilometraje'),
        )
        data['disponibles'] = qs.filter(estado='DISPONIBLE', disponible=True).count()
        data['alquilados'] = qs.filter(estado='ALQUILADO').count()
        data['mantenimiento'] = qs.filter(estado='MANTENIMIENTO').count()
        data['fuera_servicio'] = qs.filter(estado='FUERA_SERVICIO').count()
        if data['avg_precio']:
            data['avg_precio'] = round(float(data['avg_precio']), 2)
        return Response(data)
