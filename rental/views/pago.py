# rental/views/pago.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from rental.models import Pago
from rental.serializers.pago import PagoSerializer
from rental.permissions import IsStaffOrReadOnly
from rental.filters import PagoFilter
from rental.pagination import StandardPagination


class PagoViewSet(viewsets.ModelViewSet):
    serializer_class   = PagoSerializer
    permission_classes = [IsAuthenticated, IsStaffOrReadOnly]
    pagination_class   = StandardPagination
    filter_backends    = [DjangoFilterBackend, OrderingFilter]
    filterset_class    = PagoFilter
    ordering_fields    = ['fecha_pago', 'created_at']
    ordering           = ['-created_at']

    def get_queryset(self):
        if self.request.user.is_staff:
            return Pago.objects.select_related('alquiler', 'metodo_detalle').all()
        return Pago.objects.select_related('alquiler').filter(alquiler__usuario_responsable=self.request.user)

    @action(detail=True, methods=['post'], url_path='procesar')
    def procesar(self, request, pk=None):
        pago = self.get_object()
        if pago.estado != 'PENDIENTE':
            return Response(
                {'error': f'Cannot process a payment with status "{pago.estado}".'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        from datetime import datetime
        pago.estado = 'PAGADO'
        pago.fecha_pago = datetime.now()
        pago.save(update_fields=['estado', 'fecha_pago'])
        return Response(PagoSerializer(pago).data)

    @action(detail=True, methods=['post'], url_path='anular')
    def anular(self, request, pk=None):
        pago = self.get_object()
        if pago.estado == 'ANULADO':
            return Response(
                {'error': 'Payment is already annulled.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        pago.estado = 'ANULADO'
        pago.save(update_fields=['estado'])
        return Response(PagoSerializer(pago).data)

    @action(
        detail=False,
        methods=['get'],
        url_path='stats',
    )
    def stats(self, request):
        from django.db.models import Count, Sum
        qs = Pago.objects.all()
        totals = qs.aggregate(
            total_pagos = Count('id'),
            total_monto = Sum('monto'),
        )
        by_estado = {
            s: qs.filter(estado=s).count()
            for s, _ in Pago.ESTADO_CHOICES
        }
        return Response({
            'total_pagos': totals['total_pagos'],
            'total_monto': float(totals['total_monto'] or 0),
            'by_estado': by_estado,
        })
