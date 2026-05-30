# rental/views/alquiler.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from rental.models import Alquiler
from rental.serializers.alquiler import AlquilerSerializer
from rental.permissions import IsStaffOrReadOnly
from rental.filters import AlquilerFilter
from rental.pagination import StandardPagination


class AlquilerViewSet(viewsets.ModelViewSet):
    serializer_class   = AlquilerSerializer
    permission_classes = [IsAuthenticated, IsStaffOrReadOnly]
    pagination_class   = StandardPagination
    filter_backends    = [DjangoFilterBackend, OrderingFilter]
    filterset_class    = AlquilerFilter
    ordering_fields    = ['fecha_inicio', 'fecha_fin', 'created_at']
    ordering           = ['-created_at']

    def get_queryset(self):
        if self.request.user.is_staff:
            return (
                Alquiler.objects
                .select_related('cliente', 'vehiculo', 'usuario_responsable')
                .prefetch_related('reserva')
                .all()
            )
        return (
            Alquiler.objects
            .filter(usuario_responsable=self.request.user)
            .select_related('cliente', 'vehiculo')
            .prefetch_related('reserva')
        )

    def perform_create(self, serializer):
        serializer.save(usuario_responsable=self.request.user)

    @action(detail=True, methods=['post'], url_path='finalizar')
    def finalizar(self, request, pk=None):
        alquiler = self.get_object()
        if alquiler.estado != 'ACTIVO':
            return Response(
                {'error': f'Cannot finalize a rental with status "{alquiler.estado}".'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        from datetime import date
        alquiler.estado = 'FINALIZADO'
        alquiler.fecha_devolucion = date.today()
        alquiler.calcular_total()
        return Response(AlquilerSerializer(alquiler).data)

    @action(detail=True, methods=['post'], url_path='cancelar')
    def cancelar(self, request, pk=None):
        alquiler = self.get_object()
        if alquiler.estado == 'FINALIZADO':
            return Response(
                {'error': 'Cannot cancel a finalized rental.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        alquiler.estado = 'CANCELADO'
        alquiler.save(update_fields=['estado'])
        return Response(AlquilerSerializer(alquiler).data)

    @action(
        detail=False,
        methods=['get'],
        url_path='stats',
    )
    def stats(self, request):
        from django.db.models import Count, Sum
        qs = Alquiler.objects.all()
        totals = qs.aggregate(
            total_alquileres = Count('id'),
            total_ingresos = Sum('total'),
        )
        by_estado = {
            s: qs.filter(estado=s).count()
            for s, _ in Alquiler.ESTADO_CHOICES
        }
        return Response({
            'total_alquileres': totals['total_alquileres'],
            'total_ingresos': float(totals['total_ingresos'] or 0),
            'by_estado': by_estado,
        })
