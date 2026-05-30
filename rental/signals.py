# rental/signals.py
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import Alquiler, Vehiculo, Mantenimiento


@receiver(pre_save, sender=Alquiler)
def actualizar_estado_vehiculo_alquiler(sender, instance, **kwargs):
    """
    Signal para actualizar automáticamente el estado del vehículo cuando cambia el estado del alquiler.
    """
    if instance.pk:
        try:
            old_instance = Alquiler.objects.get(pk=instance.pk)
            # Si el estado cambia a ACTIVO, marcar vehículo como ALQUILADO
            if old_instance.estado != 'ACTIVO' and instance.estado == 'ACTIVO':
                instance.vehiculo.estado = 'ALQUILADO'
                instance.vehiculo.disponible = False
                instance.vehiculo.save(update_fields=['estado', 'disponible'])
            
            # Si el estado cambia a FINALIZADO, marcar vehículo como DISPONIBLE
            elif old_instance.estado != 'FINALIZADO' and instance.estado == 'FINALIZADO':
                instance.vehiculo.estado = 'DISPONIBLE'
                instance.vehiculo.disponible = True
                instance.vehiculo.save(update_fields=['estado', 'disponible'])
        except Alquiler.DoesNotExist:
            pass


@receiver(pre_save, sender=Mantenimiento)
def actualizar_estado_vehiculo_mantenimiento(sender, instance, **kwargs):
    """
    Signal para actualizar automáticamente el estado del vehículo cuando está en mantenimiento.
    """
    if instance.pk:
        try:
            old_instance = Mantenimiento.objects.get(pk=instance.pk)
            # Si el estado cambia a EN_PROCESO, marcar vehículo como MANTENIMIENTO
            if old_instance.estado != 'EN_PROCESO' and instance.estado == 'EN_PROCESO':
                instance.vehiculo.estado = 'MANTENIMIENTO'
                instance.vehiculo.disponible = False
                instance.vehiculo.save(update_fields=['estado', 'disponible'])
            
            # Si el estado cambia a COMPLETADO, marcar vehículo como DISPONIBLE
            elif old_instance.estado != 'COMPLETADO' and instance.estado == 'COMPLETADO':
                instance.vehiculo.estado = 'DISPONIBLE'
                instance.vehiculo.disponible = True
                instance.vehiculo.save(update_fields=['estado', 'disponible'])
        except Mantenimiento.DoesNotExist:
            pass
