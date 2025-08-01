from django.db import models
from django.utils import timezone
import uuid


class Process(models.Model):
    PROCESS_TYPES = [
        ('premium_subscription', 'Premium Subscription'),
        # Podés agregar más tipos en el futuro
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    process_type = models.CharField(max_length=100, choices=PROCESS_TYPES)
    user_id = models.CharField(max_length=255)
    status = models.CharField(max_length=50, default='pending')  # pending, running, success, failed
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.process_type} - {self.user_id}'


class Task(models.Model):
    TASK_STATUSES = [
        ('pending', 'Pending'),
        ('running', 'Running'),
        ('success', 'Success'),
        ('failed', 'Failed'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    process = models.ForeignKey(Process, related_name='tasks', on_delete=models.CASCADE)
    task_name = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=TASK_STATUSES, default='pending')
    started_at = models.DateTimeField(null=True, blank=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    error_message = models.TextField(blank=True, null=True)

    def start(self):
        self.status = 'running'
        self.started_at = timezone.now()
        self.save()

    def complete(self, success=True, error=None):
        self.status = 'success' if success else 'failed'
        self.ended_at = timezone.now()
        if error:
            self.error_message = str(error)
        self.save()

    def __str__(self):
        return f'{self.task_name} - {self.status}'
