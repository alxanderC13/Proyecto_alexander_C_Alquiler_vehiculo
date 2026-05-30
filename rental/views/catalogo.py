# rental/views/catalogo.py
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from rental.models import CategoriaVehiculo, TipoMantenimiento, MetodoPago
from rental.serializers.catalogo import (
    CategoriaVehiculoSerializer,
    TipoMantenimientoSerializer,
    MetodoPagoSerializer,
)
from rental.permissions import IsStaffOrReadOnly
from rental.filters import CategoriaVehiculoFilter, TipoMantenimientoFilter, MetodoPagoFilter
from rental.pagination import StandardPagination


class CategoriaVehiculoViewSet(viewsets.ModelViewSet):
    queryset           = CategoriaVehiculo.objects.all()
    serializer_class   = CategoriaVehiculoSerializer
    permission_classes = [IsStaffOrReadOnly]
    pagination_class   = StandardPagination
    filter_backends    = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class    = CategoriaVehiculoFilter
    search_fields      = ['nombre', 'descripcion']
    ordering_fields    = ['nombre', 'created_at']
    ordering           = ['nombre']


class TipoMantenimientoViewSet(viewsets.ModelViewSet):
    queryset           = TipoMantenimiento.objects.all()
    serializer_class   = TipoMantenimientoSerializer
    permission_classes = [IsStaffOrReadOnly]
    pagination_class   = StandardPagination
    filter_backends    = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class    = TipoMantenimientoFilter
    search_fields      = ['nombre', 'descripcion']
    ordering_fields    = ['nombre', 'created_at']
    ordering           = ['nombre']


class MetodoPagoViewSet(viewsets.ModelViewSet):
    queryset           = MetodoPago.objects.all()
    serializer_class   = MetodoPagoSerializer
    permission_classes = [IsStaffOrReadOnly]
    pagination_class   = StandardPagination
    filter_backends    = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class    = MetodoPagoFilter
    search_fields      = ['nombre', 'descripcion']
    ordering_fields    = ['nombre', 'created_at']
    ordering           = ['nombre']
