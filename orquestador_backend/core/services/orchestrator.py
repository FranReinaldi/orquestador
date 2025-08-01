from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db import transaction
from core.models import Process, Task
from core.services.validation import validate_user
from core.tasks import send_confirmation_email, register_external_service, notify_process_finished

VALID_PROCESS_TYPES = ['premium_subscription']

def start_process(process_type: str, user_id: str) -> Process:
    if process_type not in VALID_PROCESS_TYPES:
        raise ValidationError("Tipo de proceso inválido")

    with transaction.atomic():
        # Crear proceso
        process = Process.objects.create(
            process_type=process_type,
            user_id=user_id,
            status='running',
        )

        # Crear y ejecutar tarea de validación (síncrona)
        task_validate = Task.objects.create(
            process=process,
            task_name='validate_user',
            status='running',
            started_at=timezone.now()
        )

        try:
            validate_user(user_id)
            task_validate.status = 'success'
        except Exception as e:
            task_validate.status = 'failed'
            process.status = 'failed'
            process.save()
            task_validate.ended_at = timezone.now()
            task_validate.save()
            raise e

        task_validate.ended_at = timezone.now()
        task_validate.save()

        # Crear tarea para enviar email (asíncrona)
        task_email = Task.objects.create(
            process=process,
            task_name='send_email',
            status='pending',
            started_at=timezone.now(),
            ended_at=None
        )
        send_confirmation_email.delay(user_id, str(process.id), str(task_email.id))

        # Crear tarea para registrar en sistema externo (asíncrona)
        task_external = Task.objects.create(
            process=process,
            task_name='register_external_service',
            status='pending',
            started_at=timezone.now(),
            ended_at=None
        )
        register_external_service.delay(user_id, str(process.id), str(task_external.id))
        # Actualizar estado general del proceso, si corresponde

        process.status = 'completed'
        process.save()

        # Llamar la notificación de finalización
        notify_process_finished.delay(str(process.id))

        return process
