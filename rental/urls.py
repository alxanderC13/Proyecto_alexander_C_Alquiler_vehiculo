# rental/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from rental.views.health import health_check
from rental.views.auth import RegisterView, LogoutView
from rental.views.user import UserViewSet
from rental.views.catalogo import CategoriaVehiculoViewSet, TipoMantenimientoViewSet, MetodoPagoViewSet
from rental.views.cliente import ClienteViewSet
from rental.views.vehiculo import VehiculoViewSet
from rental.views.reserva import ReservaViewSet
from rental.views.alquiler import AlquilerViewSet
from rental.views.pago import PagoViewSet
from rental.views.mantenimiento import MantenimientoViewSet
from rental.serializers.auth import CustomTokenView

router = DefaultRouter()
router.register('users', UserViewSet, basename='user')
router.register('categorias-vehiculo', CategoriaVehiculoViewSet, basename='categoriavehiculo')
router.register('tipos-mantenimiento', TipoMantenimientoViewSet, basename='tipomantenimiento')
router.register('metodos-pago', MetodoPagoViewSet, basename='metodopago')
router.register('clientes', ClienteViewSet, basename='cliente')
router.register('vehiculos', VehiculoViewSet, basename='vehiculo')
router.register('reservas', ReservaViewSet, basename='reserva')
router.register('alquileres', AlquilerViewSet, basename='alquiler')
router.register('pagos', PagoViewSet, basename='pago')
router.register('mantenimientos', MantenimientoViewSet, basename='mantenimiento')

urlpatterns = [
    path('health/', health_check),
    path('auth/register/', RegisterView.as_view()),
    path('auth/login/', CustomTokenView.as_view()),
    path('auth/token/refresh/', TokenRefreshView.as_view()),
    path('auth/token/verify/', TokenVerifyView.as_view()),
    path('auth/logout/', LogoutView.as_view()),
    path('', include(router.urls)),
]