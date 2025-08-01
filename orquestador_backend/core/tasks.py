import logging
import app
from celery import shared_task
from time import sleep
from django.utils import timezone
from core.models import Task

logger = logging.getLogger(__name__)

@shared_task(bind=True, max_retries=3, default_retry_delay=10)
def send_confirmation_email(self, user_id, process_id, task_id):

    try:
        logger.info(f"Enviando correo de confirmación para usuario {user_id}")

        # Simula demora de envío
        sleep(5)

        # Aquí va la lógica real de envío de correo
        logger.info(f"Correo enviado para usuario {user_id}")

        # Actualiza estado de la tarea en BD
        task = Task.objects.get(id=task_id)
        task.status = 'success'
        task.ended_at = timezone.now()
        task.save()

    except Exception as exc:
        logger.error(f"Error enviando correo: {exc}")
        try:
            self.retry(exc=exc)
        except self.MaxRetriesExceededError:
            # Cuando excede reintentos, marca la tarea como fallida
            task = Task.objects.get(id=task_id)
            task.status = 'failed'
            task.ended_at = timezone.now()
            task.save()


@shared_task(bind=True, max_retries=3, default_retry_delay=10)
def register_external_service(self, user_id, process_id, task_id):
    try:
        logger.info(f"Registrando suscripción en sistema externo para usuario {user_id}")

        # Simular demora de registro externo
        sleep(30)

        # Aquí iría la lógica real de registro en sistema externo
        logger.info(f"Registro externo completado para usuario {user_id}")

        task = Task.objects.get(id=task_id)
        task.status = 'success'
        task.ended_at = timezone.now()
        task.save()

    except Exception as exc:
        logger.error(f"Error en registro externo: {exc}")
        try:
            self.retry(exc=exc)
        except self.MaxRetriesExceededError:
            task = Task.objects.get(id=task_id)
            task.status = 'failed'
            task.ended_at = timezone.now()
            task.save()

@shared_task(bind=True)
def notify_process_finished(self, process_id):
    logger.info(f"Proceso {process_id} finalizado correctamente.")