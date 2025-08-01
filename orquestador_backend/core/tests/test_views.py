from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from core.models import Process, Task
from unittest import mock
from core.tasks import send_confirmation_email, register_external_service
from django.utils import timezone


class StartProcessViewTest(APITestCase):

    def test_start_process_successful(self):
        payload = {
            "process_type": "premium_subscription",
            "user_id": "user_123"
        }

        response = self.client.post("/api/process/", payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("process_id", response.data)
        self.assertEqual(response.data["status"], "running")

        # Confirmar que el proceso fue creado en la BD
        self.assertEqual(Process.objects.count(), 1)
        process = Process.objects.first()
        self.assertEqual(process.user_id, "user_123")
        self.assertEqual(process.process_type, "premium_subscription")

    def test_start_process_missing_fields(self):
        payload = {"user_id": "user_123"}  # falta process_type

        response = self.client.post("/api/process/", payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    def test_start_process_invalid_type(self):
        payload = {
            "process_type": "invalid_type",
            "user_id": "user_123"
        }

        response = self.client.post("/api/process/", payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    def test_start_process_invalid_user(self):
        payload = {
            "process_type": "premium_subscription",
            "user_id": "invalid_user"
        }

        response = self.client.post("/api/process/", payload, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "['Usuario inválido: invalid_user']")

    @mock.patch('core.tasks.sleep', return_value=None)  # evitar delay real
    @mock.patch('core.models.Task.objects.get')
    def test_send_confirmation_email_success(self, mock_get_task, mock_sleep):
        process = Process.objects.create(
            process_type='premium_subscription',
            user_id='user_123',
            status='running'
        )
        task = Task.objects.create(status='pending', process=process)
        mock_get_task.return_value = task

        send_confirmation_email("user_123", str(process.id), str(task.id))

        task.refresh_from_db()
        self.assertEqual(task.status, 'success')
        self.assertIsNotNone(task.ended_at)

    @mock.patch('core.tasks.sleep', return_value=None)  # evitar delay real
    @mock.patch('core.tasks.Task.objects.get')
    def test_register_external_service_success(self, mock_get_task, mock_sleep):
        # Crear task pendiente de prueba
        process = Process.objects.create(
            process_type='premium_subscription',
            user_id='user_123',
            status='running'
        )
        task = Task.objects.create(
            process=process,
            task_name='register_external_service',
            status='pending'
        )
        mock_get_task.return_value = task

        # Ejecutar task
        register_external_service("user_123", str(process.id), str(task.id))

        # Refrescar de BD para verificar cambios
        task.refresh_from_db()

        assert task.status == 'success'
        assert task.ended_at is not None