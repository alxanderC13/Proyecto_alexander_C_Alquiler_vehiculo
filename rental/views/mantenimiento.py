# rental/views/mantenimiento.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from rental.models import Mantenimiento
from rental.serializers.mantenimiento import MantenimientoSerializer
from rental.permissions import IsStaffOrReadOnly
from rental.filters import MantenimientoFilter
from rental.pagination import StandardPagination


class MantenimientoViewSet(viewsets.ModelViewSet):
    serializer_class   = MantenimientoSerializer
    permission_classes = [IsAuthenticated, IsStaffOrReadOnly]
    pagination_class   = StandardPagination
    filter_backends    = [DjangoFilterBackend, OrderingFilter]
    filterset_class    = MantenimientoFilter
    ordering_fields    = ['fecha_inicio', 'fecha_fin', 'created_at']
    ordering           = ['-created_at']

    def get_queryset(self):
        if self.request.user.is_staff:
            return Mantenimiento.objects.select_related('vehiculo', 'tipo_detalle').all()
        return Mantenimiento.objects.select_related('vehiculo').all()

    @action(detail=True, methods=['post'], url_path='iniciar')
    def iniciar(self, request, pk=None):
        mantenimiento = self.get_object()
        if mantenimiento.estado != 'PROGRAMADO':
            return Response(
                {'error': f'Cannot start a maintenance with status "{mantenimiento.estado}".'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        mantenimiento.estado = 'EN_PROCESO'
        mantenimiento.save(update_fields=['estado'])
        return Response(MantenimientoSerializer(mantenimiento).data)

    @action(detail=True, methods=['post'], url_path='completar')
    def completar(self, request, pk=None):
        mantenimiento = self.get_object()
        if mantenimiento.estado != 'EN_PROCESO':
            return Response(
                {'error': f'Cannot complete a maintenance with status "{mantenimiento.estado}".'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        from datetime import date
        mantenimiento.estado = 'COMPLETADO'
        mantenimiento.fecha_fin = date.today()
        mantenimiento.save(update_fields=['estado', 'fecha_fin'])
        return Response(MantenimientoSerializer(mantenimiento).data)

    @action(detail=True, methods=['post'], url_path='cancelar')
    def cancelar(self, request, pk=None):
        mantenimiento = self.get_object()
        if mantenimiento.estado == 'COMPLETADO':
            return Response(
                {'error': 'Cannot cancel a completed maintenance.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        mantenimiento.estado = 'CANCELADO'
        mantenimiento.save(update_fields=['estado'])
        return Response(MantenimientoSerializer(mantenimiento).data)

    @action(
        detail=False,
        methods=['get'],
        url_path='stats',
    )
    def stats(self, request):
        from django.db.models import Count, Sum
        qs = Mantenimiento.objects.all()
        totals = qs.aggregate(
            total_mantenimientos = Count('id'),
            total_costo = Sum('costo'),
        )
        by_estado = {
            s: qs.filter(estado=s).count()
            for s, _ in Mantenimiento.ESTADO_CHOICES
        }
        return Response({
            'total_mantenimientos': totals['total_mantenimientos'],
            'total_costo': float(totals['total_costo'] or 0),
            'by_estado': by_estado,
        })
