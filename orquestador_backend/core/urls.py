from django.urls import path
from core import views

urlpatterns = [
    path('process/', views.start_process_view, name='start-process'),
    path('process/<str:process_id>/status', views.process_status_view, name='process-status'),
]
