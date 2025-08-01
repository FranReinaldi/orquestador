from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Process, Task


@admin.register(Process)
class ProcessAdmin(admin.ModelAdmin):
    list_display = ('id', 'process_type', 'user_id', 'status', 'created_at', 'updated_at')
    search_fields = ('user_id', 'process_type', 'status')
    list_filter = ('process_type', 'status')
    ordering = ('-created_at',)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'process', 'task_name', 'status', 'started_at', 'ended_at')
    search_fields = ('task_name', 'status')
    list_filter = ('status', 'task_name')
    ordering = ('-started_at',)
