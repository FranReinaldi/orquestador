# 🧠 Orquestador

Proyecto Django + Celery que simula un orquestador de procesos. Cada proceso consta de múltiples tareas que pueden ser síncronas o asíncronas. Se incluye una suscripción premium como ejemplo de proceso compuesto.

---

## 🐳 Instrucciones para levantar el entorno

1. Clonar el repositorio y ubicarse en la raíz:

   ```bash
   git clone <REPO_URL>
   cd orquestador
   ```

2. Construir los contenedores e iniciar los servicios:

   ```bash
   docker compose up --build
   ```

3. En otra terminal, iniciar el worker de Celery:

   ```bash
   docker-compose up celery
   ```

   O seguir los logs del worker:

   ```bash
   docker-compose logs -f celery
   ```

---

## 🚀 Cómo probar la API

### 1. Iniciar un proceso

`POST /api/process/`

**Body:**

```json
{
  "process_type": "premium_subscription",
  "user_id": "user_123"
}
```

**Response:**

```json
{
  "process_id": "proc_abcd1234",
  "status": "pending"
}
```

### 2. Consultar estado del proceso

`GET /process/<process_id>/status`

**Response:**

```json
{
  "process_id": "proc_abcd1234",
  "status": "running",
  "tasks": [
    {
      "task_name": "validate_user",
      "status": "success",
      "started_at": "2025-07-20T15:00:00Z",
      "ended_at": "2025-07-20T15:00:01Z"
    },
    {
      "task_name": "send_email",
      "status": "running",
      "started_at": "2025-07-20T15:00:02Z",
      "ended_at": null
    },
    {
      "task_name": "register_external_service",
      "status": "pending",
      "started_at": null,
      "ended_at": null
    }
  ]
}
```

---

## 🧪 Ejecutar tests

```bash
docker-compose run web python manage.py test core.tests.test_views
```

---

## 🛠️ Diseño y decisiones tomadas

- **Arquitectura modular:** el código está dividido en `core/` para la lógica de negocio y `app/` para configuración del proyecto.
- **Celery + Redis:** se usa Celery como sistema de tareas y Redis como broker y backend.
- **PostgreSQL:** se eligió por ser robusto y ampliamente soportado por Django.
- **Procesos orquestados:** un proceso contiene tareas definidas, que se ejecutan en orden. Cada tarea puede ser síncrona (como validación de usuario) o asíncrona (como envío de correos).
- **Monitoreo de estado:** se guarda el estado de cada tarea en la base, lo que permite consultar el progreso en tiempo real.
- **Simulación de servicios externos:** se usan demoras (`sleep`) para simular tiempo de respuesta y logs para registrar acciones.
- **Swagger (opcional):** se usó `drf-yasg` para documentar los endpoints (Swagger UI).

---

## ✅ Requisitos previos

- Docker y Docker Compose instalados en el sistema.

---
