# rental/views/cliente.py
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count

from rental.models import Cliente
from rental.serializers.cliente import ClienteSerializer
from rental.permissions import IsStaffOrReadOnly
from rental.filters import ClienteFilter
from rental.pagination import StandardPagination


class ClienteViewSet(viewsets.ModelViewSet):
    queryset           = Cliente.objects.all()
    serializer_class   = ClienteSerializer
    permission_classes = [IsStaffOrReadOnly]
    pagination_class   = StandardPagination
    filter_backends    = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class    = ClienteFilter
    search_fields      = ['nombres', 'apellidos', 'cedula', 'email']
    ordering_fields    = ['apellidos', 'nombres', 'created_at']
    ordering           = ['apellidos', 'nombres']

    @action(
        detail=True,
        methods=['get'],
        url_path='reservas',
    )
    def reservas(self, request, pk=None):
        from rental.serializers.reserva import ReservaSerializer
        cliente = self.get_object()
        qs = cliente.reservas.all().order_by('-created_at')
        page = self.paginate_queryset(qs)
        if page is not None:
            return self.get_paginated_response(ReservaSerializer(page, many=True).data)
        return Response(ReservaSerializer(qs, many=True).data)

    @action(
        detail=True,
        methods=['get'],
        url_path='alquileres',
    )
    def alquileres(self, request, pk=None):
        from rental.serializers.alquiler import AlquilerSerializer
        cliente = self.get_object()
        qs = cliente.alquileres.all().order_by('-created_at')
        page = self.paginate_queryset(qs)
        if page is not None:
            return self.get_paginated_response(AlquilerSerializer(page, many=True).data)
        return Response(AlquilerSerializer(qs, many=True).data)

    @action(
        detail=False,
        methods=['get'],
        url_path='stats',
    )
    def stats(self, request):
        qs = Cliente.objects.all()
        return Response({
            'total':    qs.count(),
            'active':   qs.filter(estado=True).count(),
            'inactive': qs.filter(estado=False).count(),
        })
