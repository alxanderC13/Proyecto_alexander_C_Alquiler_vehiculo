# rental/views/reserva.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from rental.models import Reserva
from rental.serializers.reserva import ReservaSerializer
from rental.permissions import IsStaffOrReadOnly
from rental.filters import ReservaFilter
from rental.pagination import StandardPagination


class ReservaViewSet(viewsets.ModelViewSet):
    serializer_class   = ReservaSerializer
    permission_classes = [IsAuthenticated, IsStaffOrReadOnly]
    pagination_class   = StandardPagination
    filter_backends    = [DjangoFilterBackend, OrderingFilter]
    filterset_class    = ReservaFilter
    ordering_fields    = ['fecha_inicio', 'fecha_fin', 'created_at']
    ordering           = ['-created_at']

    def get_queryset(self):
        if self.request.user.is_staff:
            return Reserva.objects.select_related('cliente', 'vehiculo').all()
        return Reserva.objects.select_related('cliente', 'vehiculo').filter(cliente__estado=True)

    @action(detail=True, methods=['post'], url_path='confirmar')
    def confirmar(self, request, pk=None):
        reserva = self.get_object()
        if reserva.estado != 'PENDIENTE':
            return Response(
                {'error': f'Cannot confirm a reservation with status "{reserva.estado}".'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        reserva.estado = 'CONFIRMADA'
        reserva.save(update_fields=['estado'])
        return Response(ReservaSerializer(reserva).data)

    @action(detail=True, methods=['post'], url_path='cancelar')
    def cancelar(self, request, pk=None):
        reserva = self.get_object()
        if reserva.estado == 'FINALIZADA':
            return Response(
                {'error': 'Cannot cancel a finalized reservation.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        reserva.estado = 'CANCELADA'
        reserva.save(update_fields=['estado'])
        return Response(ReservaSerializer(reserva).data)

    @action(
        detail=False,
        methods=['get'],
        url_path='stats',
    )
    def stats(self, request):
        from django.db.models import Count
        qs = Reserva.objects.all()
        return Response({
            'total': qs.count(),
            'by_estado': {
                'PENDIENTE': qs.filter(estado='PENDIENTE').count(),
                'CONFIRMADA': qs.filter(estado='CONFIRMADA').count(),
                'CANCELADA': qs.filter(estado='CANCELADA').count(),
                'FINALIZADA': qs.filter(estado='FINALIZADA').count(),
            },
        })
