# rental/views/user.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from rental.models import Usuario
from rental.serializers.user import (
    UserSerializer,
    UserProfileSerializer,
    ChangePasswordSerializer,
)
from rental.pagination import StandardPagination
from rental.filters import UsuarioFilter


class UserViewSet(viewsets.ModelViewSet):
    queryset           = Usuario.objects.all().order_by('id')
    serializer_class   = UserSerializer
    permission_classes = [IsAdminUser]
    pagination_class   = StandardPagination
    filter_backends    = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class    = UsuarioFilter
    search_fields      = ['username', 'email', 'first_name', 'last_name']
    ordering_fields    = ['id', 'username', 'date_joined']
    ordering           = ['id']

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=[IsAuthenticated],
        url_path='profile',
    )
    def profile(self, request):
        if request.method == 'GET':
            return Response(
                UserProfileSerializer(request.user, context={'request': request}).data
            )
        serializer = UserProfileSerializer(
            request.user,
            data=request.data,
            partial=True,
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(
        detail=False,
        methods=['post'],
        permission_classes=[IsAuthenticated],
        url_path='change-password',
    )
    def change_password(self, request):
        serializer = ChangePasswordSerializer(
            data=request.data,
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()
        return Response({'message': 'Password updated. Please log in again.'})

    @action(
        detail=True,
        methods=['post'],
        permission_classes=[IsAdminUser],
        url_path='toggle-active',
    )
    def toggle_active(self, request, pk=None):
        user = self.get_object()
        user.estado = not user.estado
        user.save(update_fields=['estado'])
        state = 'activated' if user.estado else 'deactivated'
        return Response({'message': f'User {state}.', 'estado': user.estado})

    @action(
        detail=False,
        methods=['get'],
        permission_classes=[IsAdminUser],
        url_path='stats',
    )
    def stats(self, request):
        qs = Usuario.objects.all()
        return Response({
            'total':    qs.count(),
            'active':   qs.filter(estado=True).count(),
            'inactive': qs.filter(estado=False).count(),
            'staff':    qs.filter(is_staff=True).count(),
            'by_rol': {
                'ADMIN': qs.filter(rol='ADMIN').count(),
                'EMPLEADO': qs.filter(rol='EMPLEADO').count(),
                'CLIENTE': qs.filter(rol='CLIENTE').count(),
            },
        })