from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from core.services.orchestrator import start_process
from core.models import Process, Task
from django.core.exceptions import ValidationError

from drf_yasg.utils import swagger_auto_schema
from core.serializers import ProcessStartSerializer


@swagger_auto_schema(method='post', request_body=ProcessStartSerializer)
@api_view(['POST'])
def start_process_view(request):
    process_type = request.data.get('process_type')
    user_id = request.data.get('user_id')

    if not process_type or not user_id:
        return Response({"error": "process_type y user_id son requeridos"}, status=400)

    try:
        process = start_process(process_type, user_id)
        return Response({
            "process_id": str(process.id),
            "status": process.status
        }, status=status.HTTP_201_CREATED)
    except ValidationError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": "Error interno"}, status=500)


@api_view(['GET'])
def process_status_view(request, process_id):
    try:
        process = Process.objects.get(id=process_id)
    except Process.DoesNotExist:
        return Response(
            {"error": f"Proceso {process_id} no encontrado."},
            status=status.HTTP_404_NOT_FOUND
        )

    tasks = Task.objects.filter(process=process).order_by('started_at')

    return Response({
        "process_id": process_id,
        "status": process.status,
        "tasks": [
            {
                "task_name": t.task_name,
                "status": t.status,
                "started_at": t.started_at.isoformat() if t.started_at else None,
                "ended_at": t.ended_at.isoformat() if t.ended_at else None
            } for t in tasks
        ]
    })
